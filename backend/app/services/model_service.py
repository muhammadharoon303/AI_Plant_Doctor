import logging
from typing import Dict, Any
from app.services.model_loader import get_model_loader

logger = logging.getLogger("plant_doctor.model_service")

class ModelService:
    """Access layer for Computer Vision prediction model using ModelLoader singleton."""

    def __init__(self):
        self.model_loader = get_model_loader()

    @property
    def model_version(self) -> str:
        return self.model_loader.model_version

    def run_inference(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Executes inference via PyTorch CV model loaded in memory.
        Calculates exact softmax class probabilities and top prediction.
        """
        logger.info(f"Running computer vision model inference on {len(image_bytes)} bytes...")
        prediction = self.model_loader.engine.predict(image_bytes)
        prediction["model_version"] = self.model_version
        return prediction

_model_service_instance = ModelService()

def get_model_service() -> ModelService:
    return _model_service_instance
