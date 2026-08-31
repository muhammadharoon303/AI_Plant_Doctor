import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from database.base import Base

class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    crop_type = Column(String(100), nullable=False, index=True)
    variety = Column(String(100), nullable=True)
    planting_date = Column(DateTime, nullable=True)
    location = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="plants")
    scans = relationship("PlantScan", back_populates="plant", cascade="all, delete-orphan")
    progress_logs = relationship("PlantProgress", back_populates="plant", cascade="all, delete-orphan")

# Backward Compatibility Alias
PlantProfile = Plant

class PlantScan(Base):
    __tablename__ = "plant_scans"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    plant_id = Column(Integer, ForeignKey("plants.id", ondelete="SET NULL"), nullable=True, index=True)
    disease_id = Column(Integer, ForeignKey("diseases.id", ondelete="SET NULL"), nullable=True, index=True)
    
    image_url = Column(String(500), nullable=False)
    mask_url = Column(String(500), nullable=True)
    disease_key = Column(String(100), nullable=False, index=True)
    confidence = Column(Float, nullable=False)
    model_version = Column(String(50), default="tomato-v1.0", nullable=False)
    segmentation_status = Column(Boolean, default=True, nullable=False)
    affected_percentage = Column(Float, default=0.0, nullable=False)
    severity_stage = Column(String(50), default="Healthy", nullable=False)
    language_used = Column(String(10), default="en", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="scans")
    plant = relationship("Plant", back_populates="scans")
    disease = relationship("Disease", back_populates="scans")
    diagnosis = relationship("Diagnosis", uselist=False, back_populates="scan", cascade="all, delete-orphan")

# Backward Compatibility Alias
Scan = PlantScan

class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True, index=True)
    scan_id = Column(Integer, ForeignKey("plant_scans.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    disease_id = Column(Integer, ForeignKey("diseases.id", ondelete="SET NULL"), nullable=True, index=True)
    
    primary_diagnosis = Column(String(255), nullable=False)
    confidence_score = Column(Float, nullable=False)
    lesion_area_percentage = Column(Float, default=0.0, nullable=False)
    severity_level = Column(String(50), default="Moderate", nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    scan = relationship("PlantScan", back_populates="diagnosis")
    disease = relationship("Disease", back_populates="diagnoses")

class PlantProgress(Base):
    __tablename__ = "plant_progress"

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("plants.id", ondelete="CASCADE"), nullable=False, index=True)
    scan_id = Column(Integer, ForeignKey("plant_scans.id", ondelete="SET NULL"), nullable=True, index=True)
    
    health_status = Column(String(50), default="Healthy", nullable=False)
    affected_percentage = Column(Float, default=0.0, nullable=False)
    observations = Column(Text, nullable=True)
    log_date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    plant = relationship("Plant", back_populates="progress_logs")

# Backward Compatibility Alias
MonitoringLog = PlantProgress

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50), default="disease_alert", nullable=False) # disease_alert, reminder, system
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="notifications")
