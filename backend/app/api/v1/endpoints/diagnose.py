import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.services.diagnosis_service import DiagnosisService
from app.schemas.diagnose import DiagnosisResponse, ScanHistoryItem, ScanHistoryListResponse
from database.models.plant import PlantScan, Plant
from database.models.disease import Disease

logger = logging.getLogger("plant_doctor.api.diagnose")

router = APIRouter()
diagnosis_service = DiagnosisService()

@router.post("", response_model=DiagnosisResponse, status_code=status.HTTP_200_OK)
@router.post("/analyze", response_model=DiagnosisResponse, status_code=status.HTTP_200_OK)
async def analyze_plant_image(
    file: UploadFile = File(...),
    lang: str = Form("en"),
    plant_profile_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Main Computer Vision Plant Image Analysis Endpoint.
    """
    logger.info(f"Received image analysis request: filename='{file.filename}', lang='{lang}'")
    return await diagnosis_service.analyze_plant_image(
        file=file,
        db=db,
        lang=lang,
        plant_profile_id=plant_profile_id
    )

@router.get("/history", response_model=ScanHistoryListResponse)
def get_diagnosis_history(
    crop: Optional[str] = Query(None),
    disease: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Retrieves complete diagnosis scan history with search and filtering.
    """
    query = db.query(PlantScan)

    if crop:
        query = query.filter(PlantScan.disease_key.ilike(f"%{crop}%"))
    if disease:
        query = query.filter(PlantScan.disease_key.ilike(f"%{disease}%"))
    if q:
        search_fmt = f"%{q}%"
        query = query.filter(or_(
            PlantScan.disease_key.ilike(search_fmt),
            PlantScan.severity_stage.ilike(search_fmt)
        ))

    total = query.count()
    scans = query.order_by(PlantScan.created_at.desc()).offset(offset).limit(limit).all()

    items = []
    for s in scans:
        parts = s.disease_key.split("___")
        crop_name = parts[0].replace("_", " ").replace("(", "").replace(")", "").strip()
        disease_name = parts[1].replace("_", " ").strip() if len(parts) > 1 else "Healthy"

        plant_name = s.plant.name if s.plant else None

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
            plant_id=s.plant_id,
            plant_name=plant_name,
            created_at=s.created_at
        ))

    return ScanHistoryListResponse(total=total, items=items)

@router.get("/{id}", response_model=ScanHistoryItem)
def get_diagnosis_by_id(id: int, db: Session = Depends(get_db)):
    """
    Retrieves specific diagnosis scan history detail record.
    """
    scan = db.query(PlantScan).filter(PlantScan.id == id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Diagnosis scan record not found")

    parts = scan.disease_key.split("___")
    crop_name = parts[0].replace("_", " ").replace("(", "").replace(")", "").strip()
    disease_name = parts[1].replace("_", " ").strip() if len(parts) > 1 else "Healthy"
    plant_name = scan.plant.name if scan.plant else None

    return ScanHistoryItem(
        id=scan.id,
        scan_id=scan.id,
        disease_key=scan.disease_key,
        crop=crop_name,
        crop_name=crop_name,
        disease=disease_name,
        disease_name=disease_name,
        confidence=scan.confidence,
        model_version=scan.model_version or "tomato-v1.0",
        segmentation_status=scan.segmentation_status,
        affected_percentage=scan.affected_percentage,
        severity_stage=scan.severity_stage,
        image_url=scan.image_url,
        mask_url=scan.mask_url,
        plant_id=scan.plant_id,
        plant_name=plant_name,
        created_at=scan.created_at
    )
