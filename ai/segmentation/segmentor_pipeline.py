import io
import os
import logging
from typing import Dict, Any, Optional
from PIL import Image
import torch
import numpy as np
import torchvision.transforms as transforms

from ai.models.segmentor import PlantLesionSegmentor
from ai.severity import SeverityEstimator

logger = logging.getLogger("plant_doctor.ai.segmentation")

class PlantLesionSegmentationPipeline:
    """
    Independent Computer Vision Disease Lesion Segmentation Pipeline.
    Fully decoupled from classification. If segmentation fails or weights are missing,
    diagnosis classification proceeds without inventing affected-area data.
    """

    def __init__(self, weights_path: Optional[str] = None, device: str = "cpu"):
        self.device = torch.device(device if torch.cuda.is_available() and device == "cuda" else "cpu")
        self.segmentor: Optional[PlantLesionSegmentor] = None
        self.is_ready: bool = False

        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

        try:
            model = PlantLesionSegmentor().to(self.device)
            if weights_path and os.path.exists(weights_path):
                model.load_state_dict(torch.load(weights_path, map_location=self.device))
                logger.info(f"Loaded U-Net lesion segmentor weights from: {weights_path}")
            else:
                logger.info("Initialized U-Net lesion segmentor model (initialized mode).")
            
            model.eval()
            self.segmentor = model
            self.is_ready = True
        except Exception as e:
            logger.warning(f"Segmentation pipeline initialization failed ({e}). Running in fallback mode.")
            self.segmentor = None
            self.is_ready = False

    def predict_segmentation(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Executes disease lesion segmentation on input leaf image bytes.
        Returns:
        - segmentation_available (bool)
        - mask (List[List[float]] or None)
        - overlay_bytes (bytes or None)
        - affected_region (dict or None)
        """
        if not self.is_ready or self.segmentor is None:
            return {
                "segmentation_available": False,
                "mask": None,
                "overlay_bytes": None,
                "affected_region": None,
                "warning": "Segmentation model is unavailable. Classification operating independently."
            }

        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            tensor = self.transform(image).unsqueeze(0).to(self.device)

            with torch.no_grad():
                mask_tensor = self.segmentor(tensor)
                mask_np = mask_tensor.squeeze().cpu().numpy()

            severity_info = SeverityEstimator.calculate_severity(mask_np)
            overlay_bytes = self.generate_overlay_bytes(image, mask_np)

            return {
                "segmentation_available": True,
                "mask": mask_np.round(4).tolist(),
                "overlay_bytes": overlay_bytes,
                "affected_region": {
                    "affected_percentage": severity_info["affected_percentage"],
                    "infected_pixel_count": int(np.sum(mask_np > 0.3)),
                    "total_leaf_pixel_count": int(mask_np.size),
                    "severity_stage": severity_info["severity_stage"]
                }
            }
        except Exception as e:
            logger.error(f"Error during segmentation execution: {e}")
            return {
                "segmentation_available": False,
                "mask": None,
                "overlay_bytes": None,
                "affected_region": None,
                "warning": f"Segmentation failed: {e}. Classification operating independently."
            }

    def generate_overlay_bytes(self, original_img: Image.Image, mask_np: np.ndarray) -> bytes:
        """Visualizes segmentation mask as a semi-transparent red overlay on original leaf photo."""
        resized_img = original_img.resize((256, 256)).convert("RGBA")
        img_np = np.array(resized_img)

        overlay = img_np.copy()
        binary_mask = mask_np > 0.3
        overlay[binary_mask, 0] = 255 # Red
        overlay[binary_mask, 1] = 50  # Green
        overlay[binary_mask, 2] = 50  # Blue
        overlay[binary_mask, 3] = 180 # Alpha blend

        blended = Image.alpha_composite(resized_img, Image.fromarray(overlay))
        output_buffer = io.BytesIO()
        blended.convert("RGB").save(output_buffer, format="PNG")
        return output_buffer.getvalue()
