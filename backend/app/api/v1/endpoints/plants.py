from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.plant import (
    PlantProfileCreate, PlantProfileUpdate, PlantProfileResponse,
    PlantProgressResponse, AffectedAreaHistoryPoint, ConfidenceHistoryPoint
)
from app.schemas.diagnose import ScanHistoryItem, ScanHistoryListResponse
from database.models.plant import Plant, PlantScan
from database.models.user import User

router = APIRouter()

@router.post("", response_model=PlantProfileResponse, status_code=status.HTTP_201_CREATED)
def create_plant_profile(
    plant_in: PlantProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new plant profile linked to the authenticated farmer."""
    plant = Plant(
        user_id=current_user.id,
        name=plant_in.name,
        crop_type=plant_in.crop_type,
        variety=plant_in.variety,
        planting_date=plant_in.planting_date,
        location=plant_in.location,
        notes=plant_in.notes
    )
    db.add(plant)
    db.commit()
    db.refresh(plant)
    return plant

@router.get("", response_model=List[PlantProfileResponse])
def get_user_plants(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve all plant profiles belonging to the authenticated farmer."""
    return db.query(Plant).filter(Plant.user_id == current_user.id).order_by(Plant.created_at.desc()).all()

@router.get("/{plant_id}", response_model=PlantProfileResponse)
def get_plant_profile(
    plant_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get details of a specific plant profile."""
    plant = db.query(Plant).filter(Plant.id == plant_id, Plant.user_id == current_user.id).first()
    if not plant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant profile not found")
    return plant

@router.put("/{plant_id}", response_model=PlantProfileResponse)
def update_plant_profile(
    plant_id: int,
    plant_in: PlantProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing plant profile."""
    plant = db.query(Plant).filter(Plant.id == plant_id, Plant.user_id == current_user.id).first()
    if not plant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant profile not found")

    update_data = plant_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(plant, field, value)

    db.commit()
    db.refresh(plant)
    return plant

@router.delete("/{plant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plant_profile(
    plant_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a plant profile."""
    plant = db.query(Plant).filter(Plant.id == plant_id, Plant.user_id == current_user.id).first()
    if not plant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant profile not found")

    db.delete(plant)
    db.commit()
    return None

@router.get("/{plant_id}/scans", response_model=ScanHistoryListResponse)
def get_plant_scans(
    plant_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves chronological scan timeline for a specific plant profile."""
    plant = db.query(Plant).filter(Plant.id == plant_id, Plant.user_id == current_user.id).first()
    if not plant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant profile not found")

    scans = db.query(PlantScan).filter(PlantScan.plant_id == plant_id).order_by(PlantScan.created_at.desc()).all()

    items = []
    for s in scans:
        parts = s.disease_key.split("___")
        crop_name = parts[0].replace("_", " ").replace("(", "").replace(")", "").strip()
        disease_name = parts[1].replace("_", " ").strip() if len(parts) > 1 else "Healthy"

        items.append(ScanHistoryItem(
            id=s.id,
            scan_id=s.id,
            disease_key=s.disease_key,
            crop=crop_name,
            crop_name=crop_name,
            disease=disease_name,
            disease_name=disease_name,
            confidence=s.confidence,
            model_version=s.model_version or "tomato-v1.0",
            segmentation_status=s.segmentation_status,
            affected_percentage=s.affected_percentage,
            severity_stage=s.severity_stage,
            image_url=s.image_url,
            mask_url=s.mask_url,
            plant_id=plant.id,
            plant_name=plant.name,
            created_at=s.created_at
        ))

    return ScanHistoryListResponse(total=len(items), items=items)

@router.get("/{plant_id}/progress", response_model=PlantProgressResponse)
def get_plant_progress(
    plant_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves disease progress analytics summary for a plant profile:
    - Previous scan vs Latest scan comparison
    - Disease history timeline
    - Affected area trend over time
    - Severity history
    - Confidence history
    """
    plant = db.query(Plant).filter(Plant.id == plant_id, Plant.user_id == current_user.id).first()
    if not plant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant profile not found")

    scans = db.query(PlantScan).filter(PlantScan.plant_id == plant_id).order_by(PlantScan.created_at.desc()).all()

    items: List[ScanHistoryItem] = []
    disease_history: List[str] = []
    affected_area_history: List[AffectedAreaHistoryPoint] = []
    confidence_history: List[ConfidenceHistoryPoint] = []
    severity_history: List[str] = []

    for s in scans:
        parts = s.disease_key.split("___")
        crop_name = parts[0].replace("_", " ").replace("(", "").replace(")", "").strip()
        disease_name = parts[1].replace("_", " ").strip() if len(parts) > 1 else "Healthy"

        item = ScanHistoryItem(
            id=s.id,
            scan_id=s.id,
            disease_key=s.disease_key,
            crop=crop_name,
            crop_name=crop_name,
            disease=disease_name,
            disease_name=disease_name,
            confidence=s.confidence,
            model_version=s.model_version or "tomato-v1.0",
            segmentation_status=s.segmentation_status,
            affected_percentage=s.affected_percentage,
            severity_stage=s.severity_stage,
            image_url=s.image_url,
            mask_url=s.mask_url,
            plant_id=plant.id,
            plant_name=plant.name,
            created_at=s.created_at
        )
        items.append(item)
        disease_history.append(disease_name)
        severity_history.append(s.severity_stage)
        affected_area_history.append(AffectedAreaHistoryPoint(
            timestamp=s.created_at,
            affected_percentage=s.affected_percentage,
            severity_stage=s.severity_stage
        ))
        confidence_history.append(ConfidenceHistoryPoint(
            timestamp=s.created_at,
            confidence=s.confidence
        ))

    latest_scan = items[0] if len(items) > 0 else None
    previous_scan = items[1] if len(items) > 1 else None

    health_trend = "Insufficient Data"
    if len(items) >= 2 and latest_scan and previous_scan:
        delta = latest_scan.affected_percentage - previous_scan.affected_percentage
        if delta < -2.5:
            health_trend = "Improving"
        elif delta > 2.5:
            health_trend = "Worsening"
        else:
            health_trend = "Stable"

    return PlantProgressResponse(
        plant_id=plant.id,
        plant_name=plant.name,
        total_scans=len(items),
        latest_scan=latest_scan,
        previous_scan=previous_scan,
        disease_history=disease_history,
        affected_area_history=affected_area_history,
        confidence_history=confidence_history,
        severity_history=severity_history,
        health_trend=health_trend
    )
