import logging
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status

from app.services.image_service import ImageService
from app.services.model_service import get_model_service, ModelService
from app.services.storage import get_storage_provider
from app.schemas.diagnose import DiagnosisResponse, QualityReport
from database.models.disease import Disease
from database.models.plant import Scan

logger = logging.getLogger("plant_doctor.diagnosis_service")

class DiagnosisService:
    def __init__(self, model_service: Optional[ModelService] = None):
        self.model_service = model_service or get_model_service()

    async def analyze_plant_image(
        self,
        file: UploadFile,
        db: Session,
        lang: str = "en",
        plant_profile_id: Optional[int] = None,
    ) -> DiagnosisResponse:
        """
        Complete Diagnosis Orchestration Workflow:
        1. Validates file MIME, extension, size limit, and image integrity via ImageService.
        2. Executes AI Inference & Image Quality Validation via ModelService (PyTorch CV model).
        3. Saves image and U-Net lesion overlay mask via StorageProvider.
        4. Queries multi-lingual Disease Knowledge Base for localized treatments.
        5. Records Scan entry in database and returns structured DiagnosisResponse.
        """
        logger.info(f"Processing leaf diagnosis request for file '{file.filename}', lang='{lang}'")

        # Step 1: File & Image Validation
        image_bytes, filename, _ = await ImageService.validate_and_read_image(file)

        # Step 2: Computer Vision Inference via ModelService
        ai_result = self.model_service.run_inference(image_bytes)

        # Check Quality Validation
        if not ai_result.get("is_confident", True):
            quality_data = ai_result.get("quality", {})
            warnings_str = "; ".join(quality_data.get("warnings", ["Poor image quality"]))
            logger.warning(f"Image quality insufficient for '{filename}': {warnings_str}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image quality is insufficient. Please capture another image. ({warnings_str})"
            )

        # Step 3: Save Image & Mask Files
        storage_provider = get_storage_provider()
        image_url = storage_provider.save_file(image_bytes, filename, subfolder="scans")
        mask_url = storage_provider.save_file(
            ai_result["mask_overlay_bytes"], f"mask_{filename}.png", subfolder="masks"
        )

        # Step 4: Multi-Lingual Knowledge Base Lookup
        disease_obj = db.query(Disease).filter_by(disease_key=ai_result["disease_key"]).first()
        if not disease_obj:
            disease_obj = db.query(Disease).filter(Disease.crop_name.ilike(f"%{ai_result['crop_name']}%")).first()

        lang_code = lang.lower() if lang.lower() in ["en", "ur", "ps"] else "en"

        if disease_obj and disease_obj.translations:
            trans = disease_obj.translations.get(lang_code, disease_obj.translations.get("en", {}))
            desc = trans.get("description", "Automatic AI computer vision diagnosis.")
            symptoms = trans.get("symptoms", "Spotting, lesioning, and leaf discoloration.")
            bio_treat = trans.get("biological_treatment", "Dosage: Spray Neem Oil (0.5% concentration, 5ml per Liter water) or Bacillus subtilis (3g/L) every 7 days.")
            chem_treat = trans.get("chemical_treatment", "Dosage: Spray Copper Oxychloride 50% WP at 2.5g per Liter water OR Mancozeb 75% WP at 2.0g per Liter water every 7-10 days. Pre-Harvest Interval (PHI): 7 days.")
            prevention = trans.get("prevention", "Maintain healthy soil, proper plant spacing, and ventilation.")
            disease_name = trans.get("name", ai_result["disease_name"])
            scientific_name = disease_obj.scientific_name
            disease_id = disease_obj.id
        else:
            disease_name = ai_result["disease_name"]
            scientific_name = "Botanical Foliage"
            disease_id = None
            desc = "Automatic AI computer vision diagnosis."
            symptoms = "Leaf lesioning, discoloration, and surface spotting."
            bio_treat = "Dosage: Spray Neem Oil (0.5% concentration, 5ml per Liter water) or Bacillus subtilis (3g/L) every 7 days."
            chem_treat = "Dosage: Spray Copper Oxychloride 50% WP at 2.5g per Liter water OR Mancozeb 75% WP at 2.0g per Liter water every 7-10 days. Pre-Harvest Interval (PHI): 7 days."
            prevention = "Ensure healthy soil, proper plant spacing, and drip irrigation."

        model_ver = ai_result.get("model_version", self.model_service.model_version)
        seg_status = ai_result.get("segmentation_available", True)

        # Step 5: Save Scan Record in DB
        scan_entry = Scan(
            disease_id=disease_id,
            plant_id=plant_profile_id,
            image_url=image_url,
            mask_url=mask_url,
            disease_key=ai_result["disease_key"],
            confidence=ai_result["confidence"],
            model_version=model_ver,
            segmentation_status=seg_status,
            affected_percentage=ai_result["affected_percentage"],
            severity_stage=ai_result["severity_stage"],
            language_used=lang_code,
        )
        db.add(scan_entry)
        db.commit()
        db.refresh(scan_entry)

        quality_info = ai_result.get("quality")
        quality_report = QualityReport(
            quality_score=quality_info["quality_score"],
            quality_status=quality_info["quality_status"],
            is_acceptable=quality_info["is_acceptable"],
            warnings=quality_info["warnings"],
            recommendation=quality_info["recommendation"]
        ) if quality_info else None

        logger.info(f"Diagnosis completed for scan_id={scan_entry.id}: {disease_name} ({ai_result['severity_stage']})")

        model_ver = ai_result.get("model_version", self.model_service.model_version)
        class_probs = ai_result.get("class_probabilities")

        return DiagnosisResponse(
            scan_id=scan_entry.id,
            disease_key=ai_result["disease_key"],
            crop=ai_result["crop_name"],
            crop_name=ai_result["crop_name"],
            disease=disease_name,
            disease_name=disease_name,
            scientific_name=scientific_name,
            confidence=ai_result["confidence"],
            model_version=model_ver,
            class_probabilities=class_probs,
            affected_percentage=ai_result["affected_percentage"],
            severity_stage=ai_result["severity_stage"],
            is_healthy=ai_result["is_healthy"],
            image_url=image_url,
            mask_url=mask_url,
            description=desc,
            symptoms=symptoms,
            biological_treatment=bio_treat,
            chemical_treatment=chem_treat,
            prevention=prevention,
            created_at=scan_entry.created_at,
            quality=quality_report
        )
