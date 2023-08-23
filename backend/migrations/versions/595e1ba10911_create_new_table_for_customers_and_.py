"""create new table for customers and drivers

Revision ID: 595e1ba10911
Revises: 2464678c9a7d
Create Date: 2023-08-23 01:32:08.229959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '595e1ba10911'
down_revision = '2464678c9a7d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # # drop table customers if exist
    # op.drop_table("customers", if_exists=True)
    # create table customers

    op.create_table(
        "customers",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("customer_id", sa.String(36), unique=True),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("active", sa.Boolean, default=True),
        sa.Column("location", sa.String(5), nullable=False),
        sa.Column("destination", sa.String(5), nullable=True),
        sa.Column("driver_id", sa.String(36), unique=True)
    )

    # create table drivers
    op.create_table("drivers",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("driver_id", sa.String(36), unique=True),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("status", sa.Integer, default=True),
        sa.Column("location", sa.String(5), nullable=False),
        sa.Column("path", sa.Text(), nullable=True),
        sa.Column("path_index", sa.Integer, nullable=True),
        sa.Column("customer_id", sa.String(36), unique=True)
    )


def downgrade() -> None:
    op.drop_table("customers")
    op.drop_table("drivers")
