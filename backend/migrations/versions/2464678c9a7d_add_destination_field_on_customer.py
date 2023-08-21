"""add destination field on customer

Revision ID: 2464678c9a7d
Revises: d2433681e704
Create Date: 2023-08-22 01:06:20.344933

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2464678c9a7d'
down_revision = 'd2433681e704'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("customers", sa.Column("destination", sa.String(255), nullable=True))


def downgrade() -> None:
    op.drop_column("customers", "destination")
