"""add drivers table

Revision ID: e66d01e416f4
Revises: 1d2e6ffdc15f
Create Date: 2023-08-14 18:34:59.641649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e66d01e416f4'
down_revision = '1d2e6ffdc15f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "drivers",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("phone", sa.String(255), nullable=False),
        sa.Column("password", sa.String(255), nullable=False),
        sa.Column("license_number", sa.String(255), nullable=False)
    )


def downgrade():
    op.drop_table("drivers")
