from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class QualityReport(BaseModel):
    quality_score: float
    quality_status: str
    is_acceptable: bool
    warnings: List[str]
    recommendation: str

class QualityErrorResponse(BaseModel):
    error: str
    quality: QualityReport

class DiagnosisResponse(BaseModel):
    scan_id: int
    disease_key: str
    crop: str
    crop_name: str
    disease: str
    disease_name: str
    scientific_name: Optional[str] = None
    confidence: float
    model_version: str = "tomato-v1.0"
    class_probabilities: Optional[Dict[str, float]] = None
    affected_percentage: float
    severity_stage: str
    is_healthy: bool
    image_url: str
    mask_url: Optional[str] = None
    description: str
    symptoms: str
    biological_treatment: str
    chemical_treatment: str
    prevention: str
    created_at: datetime
    quality: Optional[QualityReport] = None

    class Config:
        from_attributes = True

class ScanHistoryItem(BaseModel):
    id: int
    scan_id: int
    disease_key: str
    crop: str
    crop_name: str
    disease: str
    disease_name: str
    confidence: float
    model_version: str = "tomato-v1.0"
    segmentation_status: bool = True
    affected_percentage: float
    severity_stage: str
    image_url: str
    mask_url: Optional[str] = None
    plant_id: Optional[int] = None
    plant_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ScanHistoryListResponse(BaseModel):
    total: int
    items: List[ScanHistoryItem]
