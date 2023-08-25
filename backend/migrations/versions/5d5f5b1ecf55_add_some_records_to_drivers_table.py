"""add some records to drivers table

Revision ID: 5d5f5b1ecf55
Revises: e66d01e416f4
Create Date: 2023-08-14 18:41:46.465869

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '5d5f5b1ecf55'
down_revision = 'e66d01e416f4'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        INSERT INTO drivers (name, phone, email, password, license_number)
        VALUES ('Nguyen Van A', '0123456789', 'nva@gmail.com', '123456', '29K1-12345');
        """
    )
    op.execute(
        """
        INSERT INTO drivers (name, phone, email, password, license_number)
        VALUES ('Tran Van B', '0987654321', 'tvb@gmail.com', '54321', '18B1-22534');
        """
    )


def downgrade():
    op.execute(
        """
        DELETE FROM drivers WHERE name = 'Nguyen Van A';
        """
    )
    op.execute(
        """
        DELETE FROM drivers WHERE name = 'Tran Van B';
        """
    )
