from typing import Optional, List
from pydantic import BaseModel

class AssistantChatRequest(BaseModel):
    message: str
    language: str = "en"
    plant_id: Optional[int] = None
    scan_id: Optional[int] = None

class AssistantSourceCitation(BaseModel):
    title: str
    organization: Optional[str] = None
    url: Optional[str] = None

class AssistantChatResponse(BaseModel):
    response: str
    language: str
    retrieved_crop: Optional[str] = None
    retrieved_disease: Optional[str] = None
    confidence_level: Optional[str] = None
    sources: List[AssistantSourceCitation] = []
    disclaimer: str = (
        "AI Assistant advice is grounded in verified agricultural extension databases. "
        "Consult a qualified extension agent or plant pathologist before applying chemical treatments."
    )
