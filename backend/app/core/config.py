import os
try:
    from pydantic_settings import BaseSettings
except ImportError:
    try:
        from pydantic import BaseSettings
    except ImportError:
        from pydantic.v1 import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Plant Doctor"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = "super-secret-key-change-in-production-environments-123456789"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./plant_doctor.db")
    
    # Storage
    STORAGE_TYPE: str = os.getenv("STORAGE_TYPE", "local") # 'local' or 's3'
    LOCAL_UPLOAD_DIR: str = os.getenv("LOCAL_UPLOAD_DIR", "uploads")
    PUBLIC_STORAGE_BASE_URL: str = os.getenv("PUBLIC_STORAGE_BASE_URL", "http://localhost:8000/uploads")
    
    # S3 Storage Config
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "ai-plant-doctor-bucket")

    # AI Model paths
    MODEL_DIR: str = os.getenv("MODEL_DIR", "ai/weights")
    CLASSIFIER_MODEL_PATH: str = os.getenv("CLASSIFIER_MODEL_PATH", "ai/weights/plant_classifier.pt")
    SEGMENTOR_MODEL_PATH: str = os.getenv("SEGMENTOR_MODEL_PATH", "ai/weights/plant_segmentor.pt")
    INFERENCE_DEVICE: str = os.getenv("INFERENCE_DEVICE", "cpu")

    class Config:
        case_sensitive = True

settings = Settings()
