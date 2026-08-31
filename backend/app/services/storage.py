import os
import uuid
from abc import ABC, abstractmethod
from app.core.config import settings

class BaseStorageProvider(ABC):
    @abstractmethod
    def save_file(self, file_bytes: bytes, filename: str, subfolder: str = "scans") -> str:
        """Saves file bytes and returns accessible public URL."""
        pass

class LocalStorageProvider(BaseStorageProvider):
    def __init__(self, upload_dir: str = settings.LOCAL_UPLOAD_DIR, base_url: str = settings.PUBLIC_STORAGE_BASE_URL):
        self.upload_dir = upload_dir
        self.base_url = base_url
        os.makedirs(self.upload_dir, exist_ok=True)

    def save_file(self, file_bytes: bytes, filename: str, subfolder: str = "scans") -> str:
        folder_path = os.path.join(self.upload_dir, subfolder)
        os.makedirs(folder_path, exist_ok=True)
        
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(folder_path, unique_name)
        
        with open(filepath, "wb") as f:
            f.write(file_bytes)
            
        relative_url = f"{subfolder}/{unique_name}"
        return f"{self.base_url}/{relative_url}"

class S3StorageProvider(BaseStorageProvider):
    def __init__(self):
        import boto3
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket = settings.S3_BUCKET_NAME

    def save_file(self, file_bytes: bytes, filename: str, subfolder: str = "scans") -> str:
        unique_name = f"{subfolder}/{uuid.uuid4().hex}_{filename}"
        self.s3_client.put_object(
            Bucket=self.bucket,
            Key=unique_name,
            Body=file_bytes,
            ContentType="image/png"
        )
        return f"https://{self.bucket}.s3.{settings.AWS_REGION}.amazonaws.com/{unique_name}"

def get_storage_provider() -> BaseStorageProvider:
    if settings.STORAGE_TYPE == "s3":
        return S3StorageProvider()
    return LocalStorageProvider()
