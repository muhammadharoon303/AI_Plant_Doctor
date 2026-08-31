"""Initial Schema Migration for AI Plant Doctor (12 Models)

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-08-31 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 1. users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.String(length=36), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('language_preference', sa.String(length=10), nullable=False, server_default='en'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('is_admin', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('uuid')
    )
    op.create_index('idx_user_email_active', 'users', ['email', 'is_active'])

    # 2. diseases
    op.create_table(
        'diseases',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.String(length=36), nullable=True),
        sa.Column('disease_key', sa.String(length=100), nullable=False),
        sa.Column('scientific_name', sa.String(length=255), nullable=True),
        sa.Column('crop_name', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False, server_default='fungal'),
        sa.Column('severity_default', sa.String(length=50), nullable=False, server_default='Moderate'),
        sa.Column('translations', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('disease_key'),
        sa.UniqueConstraint('uuid')
    )
    op.create_index('idx_disease_crop', 'diseases', ['crop_name'])

    # 3. symptoms
    op.create_table(
        'symptoms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('disease_id', sa.Integer(), nullable=False),
        sa.Column('symptom_text', sa.Text(), nullable=False),
        sa.Column('stage', sa.String(length=50), nullable=False, server_default='Early'),
        sa.Column('affected_organ', sa.String(length=50), nullable=False, server_default='Leaf'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['disease_id'], ['diseases.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 4. disease_causes
    op.create_table(
        'disease_causes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('disease_id', sa.Integer(), nullable=False),
        sa.Column('pathogen_type', sa.String(length=50), nullable=False),
        sa.Column('pathogen_name', sa.String(length=255), nullable=True),
        sa.Column('environmental_factors', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['disease_id'], ['diseases.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 5. management_recommendations
    op.create_table(
        'management_recommendations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('disease_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('action_type', sa.String(length=50), nullable=False, server_default='Preventive'),
        sa.Column('priority', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['disease_id'], ['diseases.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 6. treatment_options
    op.create_table(
        'treatment_options',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('disease_id', sa.Integer(), nullable=False),
        sa.Column('treatment_type', sa.String(length=50), nullable=False),
        sa.Column('active_ingredient', sa.String(length=255), nullable=True),
        sa.Column('dosage_instruction', sa.Text(), nullable=True),
        sa.Column('safety_period_days', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['disease_id'], ['diseases.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 7. knowledge_sources
    op.create_table(
        'knowledge_sources',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('disease_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('author_organization', sa.String(length=255), nullable=True),
        sa.Column('source_url', sa.String(length=500), nullable=True),
        sa.Column('publication_year', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['disease_id'], ['diseases.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 8. plants
    op.create_table(
        'plants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.String(length=36), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('crop_type', sa.String(length=100), nullable=False),
        sa.Column('variety', sa.String(length=100), nullable=True),
        sa.Column('planting_date', sa.DateTime(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('uuid')
    )
    op.create_index('idx_plant_crop_user', 'plants', ['crop_type', 'user_id'])

    # 9. plant_scans
    op.create_table(
        'plant_scans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.String(length=36), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('plant_id', sa.Integer(), nullable=True),
        sa.Column('disease_id', sa.Integer(), nullable=True),
        sa.Column('image_url', sa.String(length=500), nullable=False),
        sa.Column('mask_url', sa.String(length=500), nullable=True),
        sa.Column('disease_key', sa.String(length=100), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('affected_percentage', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('severity_stage', sa.String(length=50), nullable=False, server_default='Healthy'),
        sa.Column('language_used', sa.String(length=10), nullable=False, server_default='en'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['disease_id'], ['diseases.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['plant_id'], ['plants.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('uuid')
    )

    # 10. diagnoses
    op.create_table(
        'diagnoses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.String(length=36), nullable=True),
        sa.Column('scan_id', sa.Integer(), nullable=False),
        sa.Column('disease_id', sa.Integer(), nullable=True),
        sa.Column('primary_diagnosis', sa.String(length=255), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=False),
        sa.Column('lesion_area_percentage', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('severity_level', sa.String(length=50), nullable=False, server_default='Moderate'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['disease_id'], ['diseases.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['scan_id'], ['plant_scans.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('scan_id'),
        sa.UniqueConstraint('uuid')
    )

    # 11. plant_progress
    op.create_table(
        'plant_progress',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('plant_id', sa.Integer(), nullable=False),
        sa.Column('scan_id', sa.Integer(), nullable=True),
        sa.Column('health_status', sa.String(length=50), nullable=False, server_default='Healthy'),
        sa.Column('affected_percentage', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('observations', sa.Text(), nullable=True),
        sa.Column('log_date', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['plant_id'], ['plants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['scan_id'], ['plant_scans.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )

    # 12. notifications
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.String(length=36), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False, server_default='disease_alert'),
        sa.Column('is_read', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('uuid')
    )

def downgrade() -> None:
    op.drop_table('notifications')
    op.drop_table('plant_progress')
    op.drop_table('diagnoses')
    op.drop_table('plant_scans')
    op.drop_table('plants')
    op.drop_table('knowledge_sources')
    op.drop_table('treatment_options')
    op.drop_table('management_recommendations')
    op.drop_table('disease_causes')
    op.drop_table('symptoms')
    op.drop_table('diseases')
    op.drop_table('users')
