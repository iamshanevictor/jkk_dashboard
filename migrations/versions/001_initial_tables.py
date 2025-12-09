"""Create initial tables

Revision ID: 001_initial_tables
Revises: 
Create Date: 2025-09-23 02:15:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'clusters',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('competitor_urls', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )

    op.create_table(
        'properties',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('unit_id', sa.String(length=50), nullable=False),
        sa.Column('property_name', sa.String(length=100), nullable=False),
        sa.Column('bedrooms', sa.Integer(), nullable=False),
        sa.Column('bathrooms', sa.Float(), nullable=False),
        sa.Column('max_guests', sa.Integer(), nullable=False),
        sa.Column('amenities', sa.Text(), nullable=True),
        sa.Column('quality_keywords', sa.Text(), nullable=True),
        sa.Column('cluster_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['cluster_id'], ['clusters.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('unit_id'),
    )

    op.create_table(
        'price_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('property_id', sa.Integer(), nullable=False),
        sa.Column('our_listed_price', sa.Float(), nullable=False),
        sa.Column('comp_avg_price', sa.Float(), nullable=False),
        sa.Column('was_booked', sa.Boolean(), nullable=False),
        sa.Column('final_price_paid', sa.Float(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('day_of_week', sa.String(length=10), nullable=False),
        sa.Column('lead_time', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('price_logs')
    op.drop_table('properties')
    op.drop_table('clusters')
