"""remove_cluster_table_and_cluster_id_column

Revision ID: 6fc9196190ae
Revises: 4f124afac230
Create Date: 2025-09-28 00:30:45.511025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fc9196190ae'
down_revision = '4f124afac230'
branch_labels = None
depends_on = None


def upgrade():
    # Remove cluster_id column from property table
    op.drop_column('property', 'cluster_id')
    
    # Drop the cluster table
    op.drop_table('cluster')


def downgrade():
    # Recreate cluster table
    op.create_table('cluster',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('competitor_urls', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Recreate cluster_id column in property table
    op.add_column('property', sa.Column('cluster_id', sa.String(length=50), nullable=False))
    op.create_foreign_key(None, 'property', 'cluster', ['cluster_id'], ['name'])
