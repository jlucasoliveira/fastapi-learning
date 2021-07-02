"""create_cleanings_table
Revision ID: 34b3a977eb60
Revises: 
Create Date: 2021-06-28 15:07:01.155885

"""

from alembic import op
import sqlalchemy as sa


revision = "34b3a977eb60"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cleanings",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("cleaning_type", sa.Text, nullable=False, server_default="spot_clean"),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("cleanings")
