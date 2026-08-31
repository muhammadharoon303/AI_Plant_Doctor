import io
from typing import Dict, Any, List, Tuple
from PIL import Image, ImageStat, ImageFilter
import numpy as np

class ImageQualityValidator:
    """
    Modular Image Quality Validation Service.
    Evaluates image format, resolution, blur/sharpness, brightness,
    extreme darkness/overexposure, and plant/green leaf content.
    
    Can be replaced or upgraded with a deep learning quality model
    without modifying downstream pipelines.
    """
    def __init__(self, min_resolution: int = 224, blur_threshold: float = 8.0):
        self.min_resolution = min_resolution
        self.blur_threshold = blur_threshold

    def validate_image_bytes(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Validates raw image bytes and returns a comprehensive quality report.
        """
        warnings: List[str] = []
        scores: List[float] = []
        is_critical_failure = False

        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except Exception:
            return {
                "quality_score": 0.0,
                "quality_status": "POOR",
                "is_acceptable": False,
                "warnings": ["Invalid or corrupted image format."],
                "recommendation": "Please upload a valid JPEG, PNG, or WebP image."
            }

        width, height = image.size
        img_format = image.format or "JPEG"

        # 1. Format Check
        if img_format.upper() not in ["JPEG", "JPG", "PNG", "WEBP"]:
            warnings.append(f"Unsupported format '{img_format}'. Use JPEG or PNG.")
            scores.append(0.5)
        else:
            scores.append(1.0)

        # 2. Resolution Check
        if width < self.min_resolution or height < self.min_resolution:
            warnings.append(f"Low resolution ({width}x{height}). Recommended minimum is 224x224.")
            scores.append(0.4)
            is_critical_failure = True
        else:
            scores.append(1.0)

        # 3. Brightness & Extreme Lighting Check
        stat = ImageStat.Stat(image.convert("L"))
        mean_brightness = stat.mean[0]  # Range 0-255

        if mean_brightness < 30:
            warnings.append("Image is too dark (underexposed).")
            scores.append(0.1)
            is_critical_failure = True
        elif mean_brightness > 225:
            warnings.append("Image is overexposed (too bright).")
            scores.append(0.2)
            is_critical_failure = True
        elif mean_brightness < 50 or mean_brightness > 200:
            warnings.append("Lighting is sub-optimal.")
            scores.append(0.7)
        else:
            scores.append(1.0)

        # 4. Blur / Sharpness Metric (Gradient Variance)
        gray_np = np.array(image.convert("L"), dtype=np.float32)
        std_intensity = float(np.std(gray_np))
        gy, gx = np.gradient(gray_np)
        gnorm = np.sqrt(gx**2 + gy**2)
        blur_score = float(np.var(gnorm))

        # Only evaluate blur on textured images (std > 5.0)
        if std_intensity > 5.0 and blur_score < self.blur_threshold:
            warnings.append("Image appears blurry or out of focus.")
            scores.append(0.2)
            is_critical_failure = True
        elif std_intensity > 5.0 and blur_score < self.blur_threshold * 2:
            warnings.append("Slight motion blur detected.")
            scores.append(0.7)
        else:
            scores.append(1.0)

        # 5. Plant-related / Green Leaf Content Check
        rgb_np = np.array(image, dtype=np.float32)
        r, g, b = rgb_np[:, :, 0], rgb_np[:, :, 1], rgb_np[:, :, 2]
        
        green_mask = (g > r) & (g > b) & (g > 30)
        green_ratio = float(np.mean(green_mask))

        if green_ratio < 0.05:
            warnings.append("Image does not appear to contain a plant leaf.")
            scores.append(0.1)
            is_critical_failure = True
        elif green_ratio < 0.12:
            warnings.append("Low plant leaf content visible in frame.")
            scores.append(0.6)
        else:
            scores.append(1.0)

        # Overall Score Calculation
        overall_score = float(np.mean(scores))
        overall_score = max(0.0, min(1.0, round(overall_score, 2)))

        # Quality Status Determination
        if is_critical_failure or overall_score < 0.4:
            status = "POOR"
            recommendation = "Image quality is insufficient. Please capture another image."
            is_acceptable = False
        elif overall_score >= 0.8 and len(warnings) == 0:
            status = "EXCELLENT"
            recommendation = "Image quality is excellent for PyTorch AI diagnosis."
            is_acceptable = True
        elif overall_score >= 0.6:
            status = "GOOD"
            recommendation = "Image quality is good. Analysis will proceed."
            is_acceptable = True
        else:
            status = "FAIR"
            recommendation = "Image quality is fair. Retake in better lighting for highest accuracy."
            is_acceptable = True

        return {
            "quality_score": overall_score,
            "quality_status": status,
            "is_acceptable": is_acceptable,
            "warnings": warnings,
            "recommendation": recommendation,
            "metrics": {
                "resolution": f"{width}x{height}",
                "brightness": round(mean_brightness, 1),
                "blur_score": round(blur_score, 1),
                "plant_ratio": round(green_ratio, 2),
            }
        }
