import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import engine
from database.base import Base
from database.seeds.seed_data import seed_diseases
from app.core.database import SessionLocal
from app.api.v1.router import api_router
from app.api.v1.endpoints import diagnose, plants

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Seed Initial Knowledge Base
with SessionLocal() as session:
    seed_diseases(session)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Local Upload Directory for uploaded scan & mask images
os.makedirs(settings.LOCAL_UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.LOCAL_UPLOAD_DIR), name="uploads")

# Mount API Routers
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(diagnose.router, prefix="/api/diagnosis", tags=["Plant Diagnosis"])
app.include_router(plants.router, prefix="/api/plants", tags=["Plant Profiles Management"])

@app.get("/")
def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "Online",
        "docs_url": "/docs"
    }
