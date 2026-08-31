import os
import json
import logging
from typing import Dict, Any, Optional
import numpy as np

logger = logging.getLogger("plant_doctor.ai.severity")

DEFAULT_SEVERITY_CONFIG = {
    "min_quality_score": 0.40,
    "min_segmentation_confidence": 0.30,
    "default_thresholds": {
        "low_max": 10.0,       # 0.0% - 10.0% -> Low
        "moderate_max": 25.0,  # 10.0% - 25.0% -> Moderate
        "high_max": 50.0,      # 25.0% - 50.0% -> High
                               # > 50.0% -> Severe
    },
    "disease_overrides": {
        "Tomato___Late_blight": {
            "low_max": 5.0,
            "moderate_max": 15.0,
            "high_max": 35.0,
        },
        "Potato___Late_blight": {
            "low_max": 5.0,
            "moderate_max": 15.0,
            "high_max": 35.0,
        }
    }
}

class ConfigurableSeverityEngine:
    """
    Calibratable Severity Engine evaluating leaf lesion severity.
    Thresholds are stored in configuration files or dictionaries rather than hardcoded.
    Outputs: Low, Moderate, High, Severe, or Insufficient Data.
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config = DEFAULT_SEVERITY_CONFIG.copy()

        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    loaded_config = json.load(f)
                    self.config.update(loaded_config)
                logger.info(f"Loaded custom severity configuration from {config_path}")
            except Exception as e:
                logger.warning(f"Could not load custom severity config ({e}). Using default calibratable config.")

    def evaluate_severity(
        self,
        affected_visible_area: float,
        segmentation_confidence: float = 1.0,
        image_quality_score: float = 1.0,
        disease_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluates disease severity stage based on visible area, confidence, quality, and disease-specific config.
        Outputs: Low, Moderate, High, Severe, or Insufficient Data.
        """
        min_quality = self.config.get("min_quality_score", 0.40)
        min_seg_conf = self.config.get("min_segmentation_confidence", 0.30)

        # 1. Insufficient Data Validation Safeguard
        if image_quality_score < min_quality or segmentation_confidence < min_seg_conf:
            return {
                "affected_percentage": round(affected_visible_area, 2),
                "severity_stage": "Insufficient Data",
                "is_sufficient": False,
                "reason": "Image quality or segmentation confidence is below required calibration threshold."
            }

        # 2. Select Disease-Specific or Default Thresholds
        disease_overrides = self.config.get("disease_overrides", {})
        if disease_key and disease_key in disease_overrides:
            thresholds = disease_overrides[disease_key]
        else:
            thresholds = self.config.get("default_thresholds", DEFAULT_SEVERITY_CONFIG["default_thresholds"])

        low_max = thresholds.get("low_max", 10.0)
        moderate_max = thresholds.get("moderate_max", 25.0)
        high_max = thresholds.get("high_max", 50.0)

        # 3. Categorize Severity Stage
        area = max(0.0, min(100.0, affected_visible_area))

        if area < low_max:
            severity_stage = "Low"
        elif area < moderate_max:
            severity_stage = "Moderate"
        elif area < high_max:
            severity_stage = "High"
        else:
            severity_stage = "Severe"

        return {
            "affected_percentage": round(area, 2),
            "severity_stage": severity_stage,
            "is_sufficient": True,
            "applied_thresholds": {
                "low_max": low_max,
                "moderate_max": moderate_max,
                "high_max": high_max
            }
        }

class SeverityEstimator:
    """Backward-compatible wrapper utilizing ConfigurableSeverityEngine."""

    _engine = ConfigurableSeverityEngine()

    @classmethod
    def calculate_severity(cls, mask: np.ndarray, disease_key: Optional[str] = None) -> dict:
        if mask is None or mask.size == 0:
            return {"affected_percentage": 0.0, "severity_stage": "Low", "infected_pixel_count": 0, "total_pixel_count": 0}

        binary_mask = (mask > 0.3).astype(np.uint8)
        total_pixels = binary_mask.size
        infected_pixels = int(np.sum(binary_mask))
        
        affected_pct = float((infected_pixels / total_pixels) * 100.0)
        result = cls._engine.evaluate_severity(
            affected_visible_area=affected_pct,
            segmentation_confidence=1.0,
            image_quality_score=1.0,
            disease_key=disease_key
        )

        return {
            "affected_percentage": result["affected_percentage"],
            "severity_stage": result["severity_stage"],
            "infected_pixel_count": infected_pixels,
            "total_pixel_count": total_pixels
        }
