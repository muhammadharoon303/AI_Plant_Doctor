import os
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader

from ai.evaluation.metrics import ModelEvaluator

logger = logging.getLogger("plant_doctor.ai.trainer")

class ModelTrainer:
    """Manages model training loop, validation, checkpoint saving, and best-model selection."""

    def __init__(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        class_names: List[str],
        save_dir: str = "ai/weights",
        learning_rate: float = 1e-3,
        device: Optional[str] = None,
    ):
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.class_names = class_names
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)

        if device:
            self.device = torch.device(device)
        else:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model.to(self.device)
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.AdamW(self.model.parameters(), lr=learning_rate, weight_decay=1e-4)
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(self.optimizer, mode="min", factor=0.5, patience=3)

        self.best_val_loss = float("inf")
        self.best_val_acc = 0.0

    def train_epoch(self) -> Tuple[float, float]:
        """Runs single training epoch."""
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in self.train_loader:
            images, labels = images.to(self.device), labels.to(self.device)

            self.optimizer.zero_grad()
            outputs = self.model(images)
            loss = self.criterion(outputs, labels)
            loss.backward()
            self.optimizer.step()

            running_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            correct += torch.sum(preds == labels.data).item()
            total += labels.size(0)

        epoch_loss = running_loss / (total if total > 0 else 1)
        epoch_acc = correct / (total if total > 0 else 1)
        return epoch_loss, epoch_acc

    def validate(self) -> Tuple[float, float, Dict[str, Any]]:
        """Runs validation evaluation."""
        self.model.eval()
        running_loss = 0.0
        y_true = []
        y_pred = []
        y_conf = []

        with torch.no_grad():
            for images, labels in self.val_loader:
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)

                running_loss += loss.item() * images.size(0)
                probs = F.softmax(outputs, dim=1)
                confs, preds = torch.max(probs, dim=1)

                y_true.extend(labels.cpu().numpy().tolist())
                y_pred.extend(preds.cpu().numpy().tolist())
                y_conf.extend(confs.cpu().numpy().tolist())

        total = len(y_true) if len(y_true) > 0 else 1
        val_loss = running_loss / total
        metrics = ModelEvaluator.calculate_metrics(y_true, y_pred, y_conf, self.class_names)
        val_acc = metrics["accuracy"]

        return val_loss, val_acc, metrics

    def save_checkpoint(self, epoch: int, is_best: bool = False):
        """Saves checkpoint weights and metadata json file."""
        checkpoint_path = os.path.join(self.save_dir, f"checkpoint_epoch_{epoch}.pt")
        use_tl = getattr(self.model, "use_transfer_learning", True)
        backbone = getattr(self.model, "backbone", "resnet18")
        metadata = {
            "epoch": epoch,
            "class_names": self.class_names,
            "num_classes": len(self.class_names),
            "use_transfer_learning": use_tl,
            "backbone": backbone,
            "state_dict": self.model.state_dict(),
            "optimizer_state": self.optimizer.state_dict(),
        }

        torch.save(metadata, checkpoint_path)

        if is_best:
            best_path = os.path.join(self.save_dir, "best_model.pt")
            torch.save(metadata, best_path)
            meta_path = os.path.join(self.save_dir, "model_meta.json")
            with open(meta_path, "w") as f:
                json.dump({
                    "class_names": self.class_names,
                    "num_classes": len(self.class_names),
                    "best_epoch": epoch,
                    "best_val_loss": self.best_val_loss,
                    "best_val_acc": self.best_val_acc,
                }, f, indent=2)
            logger.info(f"Updated best model checkpoint at: {best_path}")

    def train(self, num_epochs: int = 10) -> Dict[str, Any]:
        """Runs full training pipeline over specified epochs."""
        history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}

        for epoch in range(1, num_epochs + 1):
            train_loss, train_acc = self.train_epoch()
            val_loss, val_acc, metrics = self.validate()

            self.scheduler.step(val_loss)

            history["train_loss"].append(train_loss)
            history["train_acc"].append(train_acc)
            history["val_loss"].append(val_loss)
            history["val_acc"].append(val_acc)

            logger.info(
                f"Epoch [{epoch}/{num_epochs}] | "
                f"Train Loss: {train_loss:.4f} Acc: {train_acc:.4f} | "
                f"Val Loss: {val_loss:.4f} Acc: {val_acc:.4f}"
            )

            is_best = val_loss < self.best_val_loss or val_acc > self.best_val_acc
            if is_best:
                self.best_val_loss = min(val_loss, self.best_val_loss)
                self.best_val_acc = max(val_acc, self.best_val_acc)

            self.save_checkpoint(epoch, is_best=is_best)

        return history
