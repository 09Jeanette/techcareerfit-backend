"""add application contact fields

Revision ID: 3a9d4b2f7e1c
Revises: 2b7f9a1d5c3a
Create Date: 2026-08-15 11:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '3a9d4b2f7e1c'
down_revision: Union[str, Sequence[str], None] = '2b7f9a1d5c3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('applications', sa.Column('job_link', sa.VARCHAR(), nullable=True))
    op.add_column('applications', sa.Column('application_email', sa.VARCHAR(), nullable=True))
    op.add_column('applications', sa.Column('application_subject', sa.VARCHAR(), nullable=True))


def downgrade() -> None:
    op.drop_column('applications', 'application_subject')
    op.drop_column('applications', 'application_email')
    op.drop_column('applications', 'job_link')
