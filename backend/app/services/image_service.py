import io
import os
import uuid
import logging
from typing import Tuple
from PIL import Image
from fastapi import UploadFile, HTTPException, status

logger = logging.getLogger("plant_doctor.image_service")

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

class ImageService:
    @staticmethod
    async def validate_and_read_image(file: UploadFile) -> Tuple[bytes, str, Image.Image]:
        """
        Validates uploaded file MIME type, size limit, and image integrity.
        Returns raw bytes, sanitized filename, and PIL Image instance.
        """
        filename = file.filename or f"upload_{uuid.uuid4().hex[:8]}.jpg"
        ext = os.path.splitext(filename)[1].lower()

        # 1. MIME Validation
        content_type = (file.content_type or "").lower()
        if content_type not in ALLOWED_MIME_TYPES and ext not in ALLOWED_EXTENSIONS:
            logger.warning(f"Invalid MIME type '{content_type}' or extension '{ext}' for file '{filename}'")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file format '{content_type}'. Allowed formats: JPEG, PNG, WebP."
            )

        # 2. Read bytes and enforce size limit
        image_bytes = await file.read()
        if len(image_bytes) > MAX_FILE_SIZE_BYTES:
            logger.warning(f"File size {len(image_bytes)} bytes exceeds limit of {MAX_FILE_SIZE_BYTES} bytes.")
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size exceeds maximum allowed limit of 10MB."
            )

        if len(image_bytes) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded image file is empty."
            )

        # 3. Decode Image
        try:
            pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except Exception as e:
            logger.error(f"Corrupt or invalid image file: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not decode image file. File may be corrupted."
            )

        return image_bytes, filename, pil_img

    @staticmethod
    def preprocess_for_model(pil_img: Image.Image, target_size: Tuple[int, int] = (256, 256)) -> Image.Image:
        """Resizes image to target resolution while preserving aspect ratio if needed."""
        return pil_img.resize(target_size)
