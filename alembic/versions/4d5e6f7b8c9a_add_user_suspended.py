"""add user suspended flag

Revision ID: 4d5e6f7b8c9a
Revises: 3a9d4b2f7e1c
Create Date: 2026-08-15 11:50:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '4d5e6f7b8c9a'
down_revision: Union[str, Sequence[str], None] = '3a9d4b2f7e1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('suspended', sa.BOOLEAN(), nullable=True, server_default=sa.text('false')))


def downgrade() -> None:
    op.drop_column('users', 'suspended')
