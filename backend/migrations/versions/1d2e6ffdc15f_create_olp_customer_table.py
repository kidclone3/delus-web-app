"""create olp customer table

Revision ID: 1d2e6ffdc15f
Revises: 
Create Date: 2023-08-14 11:06:16.468110

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '1d2e6ffdc15f'
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
