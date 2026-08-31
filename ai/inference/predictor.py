import os
import io
import json
from typing import Dict, Any, List, Optional
from PIL import Image
import torch
import torch.nn.functional as F

from ai.models.classifier import PlantDiseaseClassifier
from ai.preprocessing.transforms import get_val_transforms

AGRICULTURAL_DISCLAIMER = (
    "AI Plant Doctor predictions are AI-assisted screening recommendations for guidance only. "
    "Please consult a qualified agricultural extension agent or plant pathologist for diagnostic confirmation "
    "and professional advice before applying chemical or cultural treatments."
)

DEFAULT_TOMATO_CLASSES = [
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites",
    "Tomato___Target_Spot",
    "Tomato___Yellow_Leaf_Curl_Virus",
    "Tomato___mosaic_virus",
    "Tomato___healthy",
]

class PlantDiseasePredictor:
    """Inference engine for Plant Disease Classification models with configurable classes and agricultural disclaimers."""

    def __init__(
        self,
        model_path: Optional[str] = None,
        class_names: Optional[List[str]] = None,
        device: Optional[str] = None
    ):
        if device:
            self.device = torch.device(device)
        else:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.class_names = class_names or DEFAULT_TOMATO_CLASSES
        self.transform = get_val_transforms(224)
        self.model = PlantDiseaseClassifier(num_classes=len(self.class_names))

        if model_path and os.path.exists(model_path):
            self.load_checkpoint(model_path)

        self.model.to(self.device)
        self.model.eval()

    def load_checkpoint(self, checkpoint_path: str):
        """Loads model weights and metadata from checkpoint."""
        checkpoint = torch.load(checkpoint_path, map_location=self.device)

        if isinstance(checkpoint, dict) and "state_dict" in checkpoint:
            if "class_names" in checkpoint:
                self.class_names = checkpoint["class_names"]

            use_tl = checkpoint.get("use_transfer_learning", True)
            backbone = checkpoint.get("backbone", "resnet18")
            self.model = PlantDiseaseClassifier(
                num_classes=len(self.class_names),
                use_transfer_learning=use_tl,
                backbone=backbone
            )
            self.model.load_state_dict(checkpoint["state_dict"])
        elif isinstance(checkpoint, dict):
            self.model.load_state_dict(checkpoint)

        self.model.to(self.device)
        self.model.eval()

    def predict_image(self, image: Image.Image) -> Dict[str, Any]:
        """Predicts plant disease from PIL Image object."""
        tensor = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            logits = self.model(tensor)
            probabilities = F.softmax(logits, dim=1)[0]
            confidence, predicted_idx = torch.max(probabilities, dim=0)

        pred_class = self.class_names[predicted_idx.item()] if predicted_idx.item() < len(self.class_names) else "Tomato___healthy"
        conf_score = float(confidence.cpu().item())

        return {
            "disease_key": pred_class,
            "confidence": round(conf_score, 4),
            "class_probabilities": {
                name: round(float(prob), 4)
                for name, prob in zip(self.class_names, probabilities.cpu().numpy())
            },
            "disclaimer": AGRICULTURAL_DISCLAIMER
        }

    def predict_bytes(self, image_bytes: bytes) -> Dict[str, Any]:
        """Predicts plant disease directly from raw image bytes."""
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        return self.predict_image(image)
