"""Remove confirmed_at column from user table.

Revision ID: remove_confirmed_at
Revises: 2dee11f76643
Create Date: 2026-03-15

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = "remove_confirmed_at"
down_revision: Union[str, None] = "add_confirmed_at"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_column("confirmed_at")


def downgrade() -> None:
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(sa.Column("confirmed_at", sa.DateTime(timezone=True), nullable=True))
