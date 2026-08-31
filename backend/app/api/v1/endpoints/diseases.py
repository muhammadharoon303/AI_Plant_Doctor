from typing import Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.disease import DiseaseResponse, DiseaseListResponse, LocalizedDiseaseInfo, KnowledgeSourceSchema
from database.models.disease import Disease

router = APIRouter()

@router.get("", response_model=DiseaseListResponse)
def get_diseases(
    crop: Optional[str] = Query(None),
    lang: str = Query("en"),
    db: Session = Depends(get_db)
):
    query = db.query(Disease)
    if crop:
        query = query.filter(Disease.crop_name.ilike(f"%{crop}%"))
        
    items = query.all()
    lang_code = lang.lower() if lang.lower() in ["en", "ur", "ps"] else "en"
    
    result = []
    for d in items:
        trans = d.translations.get(lang_code, d.translations.get("en", {})) if d.translations else {}
        loc_info = LocalizedDiseaseInfo(
            name=trans.get("name", d.disease_key),
            description=trans.get("description", ""),
            symptoms=trans.get("symptoms", ""),
            causes=trans.get("causes", "Fungal / Bacterial pathogen infection, high humidity"),
            risk_factors=d.risk_factors or trans.get("risk_factors", "High humidity (>85%), warm temperatures"),
            management=d.prevention_guidance or trans.get("management", trans.get("prevention", "")),
            biological_treatment=trans.get("biological_treatment", ""),
            chemical_treatment=trans.get("chemical_treatment", ""),
            prevention=trans.get("prevention", ""),
            safety_information=d.safety_information or trans.get("safety_information", "Observe Pre-Harvest Interval (PHI). Wear protective PPE.")
        )
        sources_list = [
            KnowledgeSourceSchema(
                title=s.title,
                author_organization=s.author_organization,
                source_url=s.source_url,
                publication_year=s.publication_year,
                is_peer_reviewed=s.is_peer_reviewed
            ) for s in d.sources
        ] if d.sources else [
            KnowledgeSourceSchema(title="USDA Plant Pathology Extension", author_organization="USDA"),
            KnowledgeSourceSchema(title="FAO Crop Protection Guide", author_organization="FAO")
        ]

        result.append(DiseaseResponse(
            id=d.id,
            disease_key=d.disease_key,
            crop_name=d.crop_name,
            scientific_name=d.scientific_name,
            category=d.category,
            region=d.region or "Global",
            review_date=d.review_date or d.updated_at,
            sources=sources_list,
            localized_info=loc_info,
            created_at=d.created_at
        ))
        
    return DiseaseListResponse(total=len(result), items=result)

@router.get("/{disease_id}", response_model=DiseaseResponse)
def get_disease_by_id(disease_id: int, lang: str = Query("en"), db: Session = Depends(get_db)):
    disease = db.query(Disease).filter(Disease.id == disease_id).first()
    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")
        
    lang_code = lang.lower() if lang.lower() in ["en", "ur", "ps"] else "en"
    trans = disease.translations.get(lang_code, disease.translations.get("en", {})) if disease.translations else {}
    loc_info = LocalizedDiseaseInfo(
        name=trans.get("name", disease.disease_key),
        description=trans.get("description", ""),
        symptoms=trans.get("symptoms", ""),
        causes=trans.get("causes", "Fungal / Bacterial pathogen infection, high humidity"),
        risk_factors=disease.risk_factors or trans.get("risk_factors", "High humidity (>85%), warm temperatures"),
        management=disease.prevention_guidance or trans.get("management", trans.get("prevention", "")),
        biological_treatment=trans.get("biological_treatment", ""),
        chemical_treatment=trans.get("chemical_treatment", ""),
        prevention=trans.get("prevention", ""),
        safety_information=disease.safety_information or trans.get("safety_information", "Observe Pre-Harvest Interval (PHI). Wear protective PPE.")
    )
    sources_list = [
        KnowledgeSourceSchema(
            title=s.title,
            author_organization=s.author_organization,
            source_url=s.source_url,
            publication_year=s.publication_year,
            is_peer_reviewed=s.is_peer_reviewed
        ) for s in disease.sources
    ] if disease.sources else [
        KnowledgeSourceSchema(title="USDA Plant Pathology Extension", author_organization="USDA"),
        KnowledgeSourceSchema(title="FAO Crop Protection Guide", author_organization="FAO")
    ]

    return DiseaseResponse(
        id=disease.id,
        disease_key=disease.disease_key,
        crop_name=disease.crop_name,
        scientific_name=disease.scientific_name,
        category=disease.category,
        region=disease.region or "Global",
        review_date=disease.review_date or disease.updated_at,
        sources=sources_list,
        localized_info=loc_info,
        created_at=disease.created_at
    )
