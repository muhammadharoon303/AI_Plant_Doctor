import io
import os
import torch
import numpy as np
from PIL import Image
import torchvision.transforms as transforms

from ai.models.classifier import PlantDiseaseClassifier
from ai.segmentation import PlantLesionSegmentationPipeline
from ai.quality import ImageQualityValidator

# Standard disease classes mapping
DISEASE_CLASSES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___healthy"
]

class PlantDoctorAIEngine:
    """
    Unified Inference Engine for Plant Disease Diagnosis, 
    Lesion Segmentation, Severity Estimation, and Image Quality Validation.
    Decoupled interface allows classification to work even if segmentation fails.
    """
    def __init__(self, classifier_path: str = None, segmentor_path: str = None, device: str = "cpu"):
        self.device = torch.device(device if torch.cuda.is_available() and device == "cuda" else "cpu")
        self.quality_validator = ImageQualityValidator()

        # Instantiate Classifier
        self.classifier = PlantDiseaseClassifier(num_classes=len(DISEASE_CLASSES)).to(self.device)
        self.classifier.eval()
        
        # Instantiate Segmentation Pipeline
        self.segmentation_pipeline = PlantLesionSegmentationPipeline(
            weights_path=segmentor_path,
            device=device
        )

        # Load classifier weights if exist
        if classifier_path and os.path.exists(classifier_path):
            try:
                self.classifier.load_state_dict(torch.load(classifier_path, map_location=self.device))
            except Exception as e:
                print(f"[AI Engine] Warning: Could not load classifier weights ({e}). Running in initialized mode.")

        # PyTorch Image Transforms
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])

    def validate_quality(self, image_bytes: bytes) -> dict:
        """Runs modular image quality validator."""
        return self.quality_validator.validate_image_bytes(image_bytes)

    def predict(self, image_bytes: bytes) -> dict:
        """
        Executes computer vision pipeline:
        1. Validates Image Quality
        2. Classifies plant disease & confidence
        3. Independently runs disease lesion segmentation if available
        """
        # Step 1: Validate Quality
        quality = self.validate_quality(image_bytes)
        if not quality["is_acceptable"]:
            return {
                "quality": quality,
                "is_confident": False,
                "error": "Image quality is insufficient. Please capture another image.",
                "warnings": quality["warnings"],
                "recommendation": quality["recommendation"],
            }

        # Step 2: Load Image & Preprocess
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        orig_width, orig_height = image.size
        
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            class_logits = self.classifier(input_tensor)
            probabilities = torch.softmax(class_logits, dim=1)[0]
            top_class_idx = torch.argmax(probabilities).item()
            confidence = float(probabilities[top_class_idx].item())
            predicted_key = DISEASE_CLASSES[top_class_idx]

        # Step 3: Run Segmentation independently
        seg_res = self.segmentation_pipeline.predict_segmentation(image_bytes)

        # Extract Crop and Disease Name
        parts = predicted_key.split("___")
        crop_name = parts[0].replace("_", " ").replace("(", "").replace(")", "").strip()
        disease_name = parts[1].replace("_", " ").strip() if len(parts) > 1 else "Healthy"

        affected_pct = 0.0
        severity_stg = "Healthy" if "healthy" in disease_name.lower() else "Moderate"
        mask_overlay_bytes = None

        if seg_res["segmentation_available"] and seg_res["affected_region"]:
            affected_pct = seg_res["affected_region"]["affected_percentage"]
            severity_stg = seg_res["affected_region"]["severity_stage"]
            mask_overlay_bytes = seg_res["overlay_bytes"]

        return {
            "quality": quality,
            "is_confident": True,
            "disease_key": predicted_key,
            "crop_name": crop_name,
            "disease_name": disease_name,
            "confidence": round(confidence, 4),
            "is_healthy": "healthy" in disease_name.lower(),
            "segmentation_available": seg_res["segmentation_available"],
            "mask": seg_res.get("mask"),
            "affected_region": seg_res.get("affected_region"),
            "affected_percentage": affected_pct,
            "severity_stage": severity_stg,
            "mask_overlay_bytes": mask_overlay_bytes,
            "image_dimensions": {"width": orig_width, "height": orig_height}
        }
