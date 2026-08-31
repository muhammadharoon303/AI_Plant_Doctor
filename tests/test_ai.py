import unittest
import io
import sys
import os
import shutil
import tempfile
import numpy as np
import torch
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

from ai.pipeline import PlantDoctorAIEngine
from ai.severity import SeverityEstimator
from ai.quality import ImageQualityValidator
from ai.dataset.plant_dataset import PlantDiseaseDataset, get_data_loaders
from ai.preprocessing.transforms import get_train_transforms, get_val_transforms
from ai.models.classifier import PlantDiseaseClassifier
from ai.evaluation.metrics import ModelEvaluator
from ai.training.trainer import ModelTrainer
from ai.inference.predictor import PlantDiseasePredictor, AGRICULTURAL_DISCLAIMER
from ai.segmentation import PlantLesionSegmentationPipeline

class TestAIPipeline(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_severity_estimator(self):
        from ai.severity import ConfigurableSeverityEngine
        engine = ConfigurableSeverityEngine()

        # 1. Normal Evaluation -> Low
        res1 = engine.evaluate_severity(affected_visible_area=4.0, segmentation_confidence=0.85, image_quality_score=0.9)
        self.assertEqual(res1["severity_stage"], "Low")

        # 2. Disease Override -> Late Blight Moderate
        res2 = engine.evaluate_severity(affected_visible_area=12.0, segmentation_confidence=0.85, image_quality_score=0.9, disease_key="Tomato___Late_blight")
        self.assertEqual(res2["severity_stage"], "Moderate")

        # 3. Low Image Quality -> Insufficient Data
        res3 = engine.evaluate_severity(affected_visible_area=25.0, segmentation_confidence=0.85, image_quality_score=0.2)
        self.assertEqual(res3["severity_stage"], "Insufficient Data")
        self.assertFalse(res3["is_sufficient"])

    def test_image_quality_validator(self):
        validator = ImageQualityValidator()
        
        # Test 1: Good Green Leaf Image
        good_img = Image.new("RGB", (300, 300), color=(40, 180, 50))
        buf1 = io.BytesIO()
        good_img.save(buf1, format="JPEG")
        res1 = validator.validate_image_bytes(buf1.getvalue())
        self.assertTrue(res1["is_acceptable"])
        self.assertIn(res1["quality_status"], ["GOOD", "EXCELLENT"])

        # Test 2: Extremely Dark Image
        dark_img = Image.new("RGB", (300, 300), color=(5, 5, 5))
        buf2 = io.BytesIO()
        dark_img.save(buf2, format="JPEG")
        res2 = validator.validate_image_bytes(buf2.getvalue())
        self.assertFalse(res2["is_acceptable"])
        self.assertEqual(res2["quality_status"], "POOR")
        self.assertTrue(any("dark" in w.lower() for w in res2["warnings"]))

    def test_segmentation_pipeline_decoupling(self):
        # 1. Test Segmentation Pipeline directly
        seg_pipeline = PlantLesionSegmentationPipeline()
        self.assertTrue(seg_pipeline.is_ready)

        img = Image.new("RGB", (256, 256), color=(45, 170, 45))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        img_bytes = buf.getvalue()

        seg_res = seg_pipeline.predict_segmentation(img_bytes)
        self.assertTrue(seg_res["segmentation_available"])
        self.assertIsNotNone(seg_res["mask"])
        self.assertIsNotNone(seg_res["affected_region"])

        # 2. Test Fallback when segmentation is disabled
        disabled_pipeline = PlantLesionSegmentationPipeline(weights_path="non_existent_weights.pt")
        # When no weights exist on file, it initializes initialized mode or fails gracefully
        fallback_res = disabled_pipeline.predict_segmentation(b"invalid_bytes")
        self.assertFalse(fallback_res["segmentation_available"])
        self.assertIsNone(fallback_res["affected_region"])

    def test_training_pipeline_and_predictor(self):
        classes = ["Tomato___Early_blight", "Tomato___healthy"]
        for cls in classes:
            cls_dir = os.path.join(self.temp_dir, cls)
            os.makedirs(cls_dir, exist_ok=True)
            for i in range(4):
                img = Image.new("RGB", (224, 224), color=(30 + i * 20, 150, 40))
                img.save(os.path.join(cls_dir, f"leaf_{i}.jpg"))

        train_tf = get_train_transforms(224)
        val_tf = get_val_transforms(224)
        train_loader, val_loader, test_loader, discovered_classes = get_data_loaders(
            data_dir=self.temp_dir,
            train_transform=train_tf,
            val_transform=val_tf,
            batch_size=2,
            val_ratio=0.25,
            test_ratio=0.25,
            class_names=classes
        )
        self.assertEqual(len(discovered_classes), 2)

        model = PlantDiseaseClassifier(num_classes=2, use_transfer_learning=False)
        trainer = ModelTrainer(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
            class_names=classes,
            save_dir=os.path.join(self.temp_dir, "weights")
        )
        history = trainer.train(num_epochs=1)
        self.assertIn("train_loss", history)

        metrics = ModelEvaluator.calculate_metrics([0, 1, 0, 1], [0, 1, 0, 0], [0.9, 0.8, 0.95, 0.6], classes)
        self.assertIn("accuracy", metrics)
        self.assertEqual(metrics["accuracy"], 0.75)
        self.assertIn("confidence_distribution", metrics)

        best_path = os.path.join(self.temp_dir, "weights", "best_model.pt")
        predictor = PlantDiseasePredictor(model_path=best_path, class_names=classes)
        test_img = Image.new("RGB", (224, 224), color=(40, 180, 50))
        pred_res = predictor.predict_image(test_img)

        self.assertIn("disease_key", pred_res)
        self.assertIn("confidence", pred_res)
        self.assertEqual(pred_res["disclaimer"], AGRICULTURAL_DISCLAIMER)

    def test_comprehensive_evaluation_reports(self):
        classes = ["Tomato___Early_blight", "Tomato___healthy"]
        for cls in classes:
            cls_dir = os.path.join(self.temp_dir, "data", cls)
            os.makedirs(cls_dir, exist_ok=True)
            for i in range(4):
                img = Image.new("RGB", (224, 224), color=(40, 160, 40))
                img.save(os.path.join(cls_dir, f"sample_{i}.jpg"))

        train_tf = get_train_transforms(224)
        val_tf = get_val_transforms(224)
        _, _, test_loader, _ = get_data_loaders(
            data_dir=os.path.join(self.temp_dir, "data"),
            train_transform=train_tf,
            val_transform=val_tf,
            batch_size=2,
            class_names=classes
        )

        model = PlantDiseaseClassifier(num_classes=2, use_transfer_learning=False)
        device = torch.device("cpu")

        report_dir = os.path.join(self.temp_dir, "reports")
        test_metrics = ModelEvaluator.evaluate_model_on_dataloader(
            model=model,
            data_loader=test_loader,
            class_names=classes,
            device=device,
            dataset_label="Unseen Test Set (Real-world Proxy)",
            output_dir=report_dir
        )

        self.assertIn("accuracy", test_metrics)
        self.assertTrue(os.path.exists(os.path.join(report_dir, "metrics.json")))
        self.assertTrue(os.path.exists(os.path.join(report_dir, "confusion_matrix.png")))
        self.assertTrue(os.path.exists(os.path.join(report_dir, "classification_report.txt")))
        self.assertTrue(os.path.exists(os.path.join(report_dir, "model_metadata.json")))

    def test_ai_engine_predict(self):
        engine = PlantDoctorAIEngine()
        
        # Create synthetic valid green leaf test image
        img = Image.new("RGB", (256, 256), color=(50, 150, 50))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        img_bytes = buf.getvalue()
        
        prediction = engine.predict(img_bytes)
        self.assertTrue(prediction.get("is_confident", True))
        self.assertIn("disease_key", prediction)
        self.assertIn("confidence", prediction)
        self.assertIn("segmentation_available", prediction)

if __name__ == "__main__":
    unittest.main()
