"""remove_season_flag_column

Revision ID: dcb369913230
Revises: 4f124afac230
Create Date: 2025-09-23 03:13:32.621460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dcb369913230'
down_revision = '4f124afac230'
branch_labels = None
depends_on = None


def upgrade():
    # Remove the season_flag column from the price_log table
    op.drop_column('price_log', 'season_flag')


def downgrade():
    # Add back the season_flag column in case we need to rollback
    op.add_column('price_log', sa.Column('season_flag', sa.String(length=50), nullable=True))
