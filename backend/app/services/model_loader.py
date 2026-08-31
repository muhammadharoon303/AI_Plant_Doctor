import os
import logging
from typing import Dict, Any, Optional
from ai.pipeline import PlantDoctorAIEngine
from app.core.config import settings

logger = logging.getLogger("plant_doctor.model_loader")

class ModelLoader:
    """
    Singleton ModelLoader that loads PyTorch Computer Vision models into memory ONCE.
    Prevents reloading model weights on every API request. Supports model versioning.
    """

    _instance: Optional["ModelLoader"] = None
    _engine: Optional[PlantDoctorAIEngine] = None
    _model_version: str = "tomato-v1.0"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
            cls._instance._initialize_models()
        return cls._instance

    def _initialize_models(self):
        logger.info("Initializing PyTorch ModelLoader (loading weights ONCE into memory)...")
        self._engine = PlantDoctorAIEngine(
            classifier_path=settings.CLASSIFIER_MODEL_PATH,
            segmentor_path=settings.SEGMENTOR_MODEL_PATH,
            device=settings.INFERENCE_DEVICE
        )
        
        # Discover version if model_meta.json exists
        meta_path = os.path.join(settings.MODEL_DIR, "model_meta.json")
        if os.path.exists(meta_path):
            import json
            try:
                with open(meta_path, "r") as f:
                    meta = json.load(f)
                    if "version" in meta:
                        self._model_version = meta["version"]
            except Exception as e:
                logger.warning(f"Could not read model metadata version: {e}")

    @property
    def engine(self) -> PlantDoctorAIEngine:
        if self._engine is None:
            self._initialize_models()
        return self._engine

    @property
    def model_version(self) -> str:
        return self._model_version

def get_model_loader() -> ModelLoader:
    return ModelLoader()
