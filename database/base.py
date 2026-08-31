from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models for Alembic autogenerate discovery
from database.models.user import User # noqa
from database.models.disease import ( # noqa
    Disease, Symptom, DiseaseCause, ManagementRecommendation, TreatmentOption, KnowledgeSource
)
from database.models.plant import ( # noqa
    Plant, PlantScan, Diagnosis, PlantProgress, Notification
)
