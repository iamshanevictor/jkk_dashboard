"""Add lead_time and season_flag to PriceLog

Revision ID: 4f124afac230
Revises: 001_initial_tables
Create Date: 2025-09-23 01:09:30.177635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f124afac230'
down_revision = '001_initial_tables'
branch_labels = None
depends_on = None


def upgrade():
    # lead_time is now included in the initial table creation, so this migration does nothing
    pass


def downgrade():
    # lead_time is now included in the initial table creation, so this migration does nothing
    pass
