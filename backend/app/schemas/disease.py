from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel

class KnowledgeSourceSchema(BaseModel):
    title: str
    author_organization: Optional[str] = None
    source_url: Optional[str] = None
    publication_year: Optional[int] = None
    is_peer_reviewed: str = "Verified"

class LocalizedDiseaseInfo(BaseModel):
    name: str
    description: str
    symptoms: str
    causes: Optional[str] = None
    risk_factors: Optional[str] = None
    management: Optional[str] = None
    biological_treatment: str
    chemical_treatment: str
    prevention: str
    safety_information: Optional[str] = None

class DiseaseResponse(BaseModel):
    id: int
    disease_key: str
    crop_name: str
    scientific_name: Optional[str]
    category: str
    region: str = "Global"
    review_date: datetime
    sources: List[KnowledgeSourceSchema] = []
    localized_info: LocalizedDiseaseInfo
    created_at: datetime

    class Config:
        from_attributes = True

class DiseaseListResponse(BaseModel):
    total: int
    items: List[DiseaseResponse]
