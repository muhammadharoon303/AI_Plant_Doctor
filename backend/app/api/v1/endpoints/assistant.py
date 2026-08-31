import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.assistant import AssistantChatRequest, AssistantChatResponse
from app.services.assistant import PlantAssistantRAGEngine

logger = logging.getLogger("plant_doctor.api.assistant")

router = APIRouter()

@router.post("", response_model=AssistantChatResponse)
def chat_with_assistant(
    request: AssistantChatRequest,
    db: Session = Depends(get_db)
):
    """
    RAG-driven AI Plant Health Assistant Endpoint.
    Pipeline:
    User Question -> Context Retrieval -> Knowledge Retrieval -> AI Response -> Safety Validation -> Answer
    """
    logger.info(f"Processing AI assistant request: '{request.message}', lang='{request.language}'")
    return PlantAssistantRAGEngine.process_query(
        db=db,
        message=request.message,
        lang=request.language,
        plant_id=request.plant_id,
        scan_id=request.scan_id
    )
