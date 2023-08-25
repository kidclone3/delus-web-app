"""add rides table

Revision ID: fe0ea0687891
Revises: 5d5f5b1ecf55
Create Date: 2023-08-15 16:36:11.348012

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'fe0ea0687891'
down_revision = '5d5f5b1ecf55'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "rides",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("car_id", sa.String(length=255), nullable=False, unique=True),
        sa.Column("location", sa.String(length=255), nullable=False),
        sa.Column("path", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("rides")
