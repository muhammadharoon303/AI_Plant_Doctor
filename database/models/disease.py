import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship
from database.base import Base

class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True, index=True)
    disease_key = Column(String(100), unique=True, index=True, nullable=False)
    scientific_name = Column(String(255), nullable=True)
    crop_name = Column(String(100), nullable=False, index=True)
    category = Column(String(50), default="fungal", nullable=False) # fungal, bacterial, viral, nutrient
    severity_default = Column(String(50), default="Moderate", nullable=False)
    region = Column(String(100), default="Global", nullable=False) # Region e.g., South Asia, North America, Global
    risk_factors = Column(Text, nullable=True) # Environmental & cultivation risk factors
    prevention_guidance = Column(Text, nullable=True) # Prevention procedures
    safety_information = Column(Text, nullable=True) # PHI, PPE, withholding guidelines
    review_date = Column(DateTime, default=datetime.utcnow, nullable=False) # Last agricultural extension review date
    translations = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    symptoms = relationship("Symptom", back_populates="disease", cascade="all, delete-orphan")
    causes = relationship("DiseaseCause", back_populates="disease", cascade="all, delete-orphan")
    recommendations = relationship("ManagementRecommendation", back_populates="disease", cascade="all, delete-orphan")
    treatments = relationship("TreatmentOption", back_populates="disease", cascade="all, delete-orphan")
    sources = relationship("KnowledgeSource", back_populates="disease", cascade="all, delete-orphan")
    scans = relationship("PlantScan", back_populates="disease")
    diagnoses = relationship("Diagnosis", back_populates="disease")

class Symptom(Base):
    __tablename__ = "symptoms"

    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer, ForeignKey("diseases.id", ondelete="CASCADE"), nullable=False, index=True)
    symptom_text = Column(Text, nullable=False)
    stage = Column(String(50), default="Early", nullable=False) # Early, Advanced, Severe
    affected_organ = Column(String(50), default="Leaf", nullable=False) # Leaf, Stem, Fruit, Root
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    disease = relationship("Disease", back_populates="symptoms")

class DiseaseCause(Base):
    __tablename__ = "disease_causes"

    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer, ForeignKey("diseases.id", ondelete="CASCADE"), nullable=False, index=True)
    pathogen_type = Column(String(50), nullable=False) # Fungus, Bacteria, Virus, Environment
    pathogen_name = Column(String(255), nullable=True)
    environmental_factors = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    disease = relationship("Disease", back_populates="causes")

class ManagementRecommendation(Base):
    __tablename__ = "management_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer, ForeignKey("diseases.id", ondelete="CASCADE"), nullable=False, index=True)
    source_id = Column(Integer, ForeignKey("knowledge_sources.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    action_type = Column(String(50), default="Preventive", nullable=False) # Preventive, Cultural, Physical
    priority = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    disease = relationship("Disease", back_populates="recommendations")
    source = relationship("KnowledgeSource")

class TreatmentOption(Base):
    __tablename__ = "treatment_options"

    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer, ForeignKey("diseases.id", ondelete="CASCADE"), nullable=False, index=True)
    source_id = Column(Integer, ForeignKey("knowledge_sources.id", ondelete="SET NULL"), nullable=True, index=True)
    treatment_type = Column(String(50), nullable=False) # Biological, Chemical, Organic
    active_ingredient = Column(String(255), nullable=True)
    dosage_instruction = Column(Text, nullable=True)
    safety_period_days = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    disease = relationship("Disease", back_populates="treatments")
    source = relationship("KnowledgeSource")

class KnowledgeSource(Base):
    __tablename__ = "knowledge_sources"

    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer, ForeignKey("diseases.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    author_organization = Column(String(255), nullable=True) # e.g. USDA, FAO, CABI
    source_url = Column(String(500), nullable=True)
    publication_year = Column(Integer, nullable=True)
    is_peer_reviewed = Column(String(20), default="Verified", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    disease = relationship("Disease", back_populates="sources")
