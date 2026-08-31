import os
import json
import logging
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader

logger = logging.getLogger("plant_doctor.ai.evaluator")

class ModelEvaluator:
    """Comprehensive Model Evaluator for Computer Vision Plant Disease Classification."""

    @staticmethod
    def calculate_metrics(
        y_true: List[int],
        y_pred: List[int],
        y_conf: List[float],
        class_names: List[str]
    ) -> Dict[str, Any]:
        y_true_np = np.array(y_true, dtype=int)
        y_pred_np = np.array(y_pred, dtype=int)
        y_conf_np = np.array(y_conf, dtype=float)

        total_samples = len(y_true_np) if len(y_true_np) > 0 else 1
        correct_mask = (y_true_np == y_pred_np)
        accuracy = float(np.sum(correct_mask) / total_samples)

        # 1. Per-Class Metrics
        num_classes = len(class_names)
        per_class = {}
        weighted_precision = 0.0
        weighted_recall = 0.0
        weighted_f1 = 0.0

        for idx, name in enumerate(class_names):
            tp = int(np.sum((y_true_np == idx) & (y_pred_np == idx)))
            fp = int(np.sum((y_true_np != idx) & (y_pred_np == idx)))
            fn = int(np.sum((y_true_np == idx) & (y_pred_np != idx)))
            support = int(np.sum(y_true_np == idx))

            precision = float(tp / (tp + fp)) if (tp + fp) > 0 else 0.0
            recall = float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
            f1 = float(2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

            per_class[name] = {
                "precision": round(precision, 4),
                "recall": round(recall, 4),
                "f1_score": round(f1, 4),
                "support": support,
            }

            weight = support / total_samples
            weighted_precision += precision * weight
            weighted_recall += recall * weight
            weighted_f1 += f1 * weight

        macro_precision = float(np.mean([m["precision"] for m in per_class.values()]))
        macro_recall = float(np.mean([m["recall"] for m in per_class.values()]))
        macro_f1 = float(np.mean([m["f1_score"] for m in per_class.values()]))

        # 2. Confusion Matrix Calculation (N x N)
        cm = np.zeros((num_classes, num_classes), dtype=int)
        for t, p in zip(y_true_np, y_pred_np):
            if 0 <= t < num_classes and 0 <= p < num_classes:
                cm[t, p] += 1

        # 3. Confidence Distribution Metrics
        mean_confidence = float(np.mean(y_conf_np)) if len(y_conf_np) > 0 else 0.0
        std_confidence = float(np.std(y_conf_np)) if len(y_conf_np) > 0 else 0.0

        correct_conf = y_conf_np[correct_mask] if len(y_conf_np) > 0 else np.array([])
        incorrect_conf = y_conf_np[~correct_mask] if len(y_conf_np) > 0 else np.array([])

        mean_correct_conf = float(np.mean(correct_conf)) if len(correct_conf) > 0 else 0.0
        mean_incorrect_conf = float(np.mean(incorrect_conf)) if len(incorrect_conf) > 0 else 0.0

        hist, bin_edges = np.histogram(y_conf_np, bins=5, range=(0.0, 1.0))
        conf_histogram = {
            f"{round(bin_edges[i], 1)}-{round(bin_edges[i+1], 1)}": int(hist[i])
            for i in range(len(hist))
        }

        return {
            "accuracy": round(accuracy, 4),
            "macro_precision": round(macro_precision, 4),
            "macro_recall": round(macro_recall, 4),
            "macro_f1": round(macro_f1, 4),
            "weighted_precision": round(weighted_precision, 4),
            "weighted_recall": round(weighted_recall, 4),
            "weighted_f1": round(weighted_f1, 4),
            "total_samples": total_samples,
            "per_class": per_class,
            "confusion_matrix": cm.tolist(),
            "confidence_distribution": {
                "mean_confidence": round(mean_confidence, 4),
                "std_confidence": round(std_confidence, 4),
                "mean_correct_confidence": round(mean_correct_conf, 4),
                "mean_incorrect_confidence": round(mean_incorrect_conf, 4),
                "confidence_bins": conf_histogram,
            }
        }

    @staticmethod
    def generate_confusion_matrix_image(
        cm_list: List[List[int]],
        class_names: List[str],
        output_path: str
    ):
        """Generates visual confusion matrix heatmap image using PIL."""
        cm = np.array(cm_list)
        num_classes = len(class_names)

        cell_size = 60
        margin = 120
        img_width = margin + num_classes * cell_size + 40
        img_height = margin + num_classes * cell_size + 40

        img = Image.new("RGB", (img_width, img_height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        draw.text((margin, 20), "Confusion Matrix Heatmap", fill=(0, 0, 0))

        max_val = np.max(cm) if np.max(cm) > 0 else 1

        for i in range(num_classes):
            for j in range(num_classes):
                val = cm[i, j]
                intensity = int(255 * (1.0 - (val / max_val)))
                color = (intensity, intensity, 255) # Blue shade

                x0 = margin + j * cell_size
                y0 = margin + i * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size

                draw.rectangle([x0, y0, x1, y1], fill=color, outline=(200, 200, 200))
                draw.text((x0 + 15, y0 + 20), str(val), fill=(0, 0, 0) if intensity > 128 else (255, 255, 255))

        for idx, name in enumerate(class_names):
            short_name = name.split("___")[-1][:8]
            draw.text((margin + idx * cell_size + 5, margin - 25), short_name, fill=(0, 0, 0))
            draw.text((10, margin + idx * cell_size + 20), short_name, fill=(0, 0, 0))

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path)
        logger.info(f"Saved confusion matrix image to: {output_path}")

    @staticmethod
    def generate_text_report(metrics_data: Dict[str, Any], dataset_label: str = "Test Set (Real-world Proxy)") -> str:
        """Generates human-readable classification text report."""
        lines = []
        lines.append("=" * 70)
        lines.append(f"AI PLANT DOCTOR - MODEL EVALUATION REPORT ({dataset_label.upper()})")
        lines.append("=" * 70)
        lines.append(f"Evaluation Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        lines.append(f"Dataset Role:    {dataset_label}")
        lines.append(f"Total Samples:   {metrics_data['total_samples']}")
        lines.append(f"Overall Accuracy:{metrics_data['accuracy'] * 100:.2f}%")
        lines.append(f"Macro F1 Score:  {metrics_data['macro_f1']:.4f}")
        lines.append(f"Weighted F1:     {metrics_data['weighted_f1']:.4f}")
        lines.append("-" * 70)

        lines.append(f"{'Class Name':<35} | {'Prec':<7} | {'Recall':<7} | {'F1':<7} | {'Support':<7}")
        lines.append("-" * 70)
        for cls_name, cls_metrics in metrics_data["per_class"].items():
            lines.append(
                f"{cls_name:<35} | "
                f"{cls_metrics['precision']:<7.4f} | "
                f"{cls_metrics['recall']:<7.4f} | "
                f"{cls_metrics['f1_score']:<7.4f} | "
                f"{cls_metrics['support']:<7}"
            )
        lines.append("-" * 70)

        conf = metrics_data.get("confidence_distribution", {})
        lines.append("CONFIDENCE DISTRIBUTION ANALYSIS:")
        lines.append(f"  Mean Confidence:          {conf.get('mean_confidence', 0.0):.4f}")
        lines.append(f"  Mean Correct Confidence:  {conf.get('mean_correct_confidence', 0.0):.4f}")
        lines.append(f"  Mean Incorrect Confidence:{conf.get('mean_incorrect_confidence', 0.0):.4f}")
        lines.append("=" * 70)
        return "\n".join(lines)

    @classmethod
    def evaluate_model_on_dataloader(
        cls,
        model: nn.Module,
        data_loader: DataLoader,
        class_names: List[str],
        device: torch.device,
        dataset_label: str = "Test Set (Real-world Proxy)",
        output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """Evaluates model on data_loader and saves evaluation reports."""
        model.eval()
        model.to(device)

        y_true = []
        y_pred = []
        y_conf = []

        with torch.no_grad():
            for images, labels in data_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                probs = F.softmax(outputs, dim=1)
                confs, preds = torch.max(probs, dim=1)

                y_true.extend(labels.cpu().numpy().tolist())
                y_pred.extend(preds.cpu().numpy().tolist())
                y_conf.extend(confs.cpu().numpy().tolist())

        metrics = cls.calculate_metrics(y_true, y_pred, y_conf, class_names)
        metrics["dataset_role"] = dataset_label

        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

            # 1. Save Metrics JSON
            json_path = os.path.join(output_dir, "metrics.json")
            with open(json_path, "w") as f:
                json.dump(metrics, f, indent=2)

            # 2. Save Confusion Matrix Image
            cm_img_path = os.path.join(output_dir, "confusion_matrix.png")
            cls.generate_confusion_matrix_image(metrics["confusion_matrix"], class_names, cm_img_path)

            # 3. Save Text Classification Report
            report_text = cls.generate_text_report(metrics, dataset_label=dataset_label)
            report_path = os.path.join(output_dir, "classification_report.txt")
            with open(report_path, "w") as f:
                f.write(report_text)

            # 4. Save Model Metadata
            meta_path = os.path.join(output_dir, "model_metadata.json")
            metadata = {
                "evaluation_date": datetime.utcnow().isoformat(),
                "dataset_role": dataset_label,
                "num_classes": len(class_names),
                "class_names": class_names,
                "overall_accuracy": metrics["accuracy"],
                "macro_f1": metrics["macro_f1"],
                "total_test_samples": metrics["total_samples"],
                "distinction_note": (
                    "Validation set was used for hyperparameter tuning & best-model checkpoint selection. "
                    "This Test Set evaluation represents an un-seen real-world proxy performance benchmark."
                )
            }
            with open(meta_path, "w") as f:
                json.dump(metadata, f, indent=2)

            logger.info(f"Saved evaluation artifacts to directory: {output_dir}")

        return metrics
