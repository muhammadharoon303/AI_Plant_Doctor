from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from app.schemas.diagnose import ScanHistoryItem

class PlantProfileCreate(BaseModel):
    name: str
    crop_type: str
    variety: Optional[str] = None
    planting_date: Optional[datetime] = None
    location: Optional[str] = None
    notes: Optional[str] = None

class PlantProfileUpdate(BaseModel):
    name: Optional[str] = None
    crop_type: Optional[str] = None
    variety: Optional[str] = None
    planting_date: Optional[datetime] = None
    location: Optional[str] = None
    notes: Optional[str] = None

class MonitoringLogResponse(BaseModel):
    id: int
    health_status: str = "Healthy"
    affected_percentage: float = 0.0
    observations: Optional[str] = None
    log_date: datetime

    class Config:
        from_attributes = True

class PlantProfileResponse(BaseModel):
    id: int
    user_id: int
    name: str
    crop_type: str
    variety: Optional[str] = None
    planting_date: Optional[datetime] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AffectedAreaHistoryPoint(BaseModel):
    timestamp: datetime
    affected_percentage: float
    severity_stage: str

class ConfidenceHistoryPoint(BaseModel):
    timestamp: datetime
    confidence: float

class PlantProgressResponse(BaseModel):
    plant_id: int
    plant_name: str
    total_scans: int
    latest_scan: Optional[ScanHistoryItem] = None
    previous_scan: Optional[ScanHistoryItem] = None
    disease_history: List[str] = []
    affected_area_history: List[AffectedAreaHistoryPoint] = []
    confidence_history: List[ConfidenceHistoryPoint] = []
    severity_history: List[str] = []
    health_trend: str = "Stable"
