from fastapi import APIRouter

from app.api.v1.endpoints import auth, diagnose, diseases, plants, assistant, admin, notifications

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(diagnose.router, prefix="/diagnose", tags=["Plant Diagnosis"])
api_router.include_router(diseases.router, prefix="/diseases", tags=["Disease Knowledge Base"])
api_router.include_router(plants.router, prefix="/plants", tags=["Plant Profiles & Monitoring"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications & Alerts"])
api_router.include_router(assistant.router, prefix="/assistant", tags=["AI Assistant"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin Dashboard"])
