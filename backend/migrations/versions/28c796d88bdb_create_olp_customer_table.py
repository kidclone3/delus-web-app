"""create olp customer table

Revision ID: 28c796d88bdb
Revises: 
Create Date: 2023-07-20 15:43:57.708105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28c796d88bdb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "olp_customer",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("school", sa.String(255), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("olp_customer")
