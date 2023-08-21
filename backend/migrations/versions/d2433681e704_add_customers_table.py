"""add customers table

Revision ID: d2433681e704
Revises: fe0ea0687891
Create Date: 2023-08-21 11:43:52.864098

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2433681e704'
down_revision = 'fe0ea0687891'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("customers",
                    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
                    sa.Column("name", sa.String(255), nullable=False),
                    sa.Column("active", sa.Boolean, nullable=False, default=True),
                    sa.Column("location", sa.JSON, nullable=False),
                    )


def downgrade() -> None:
    op.drop_table("customers")
