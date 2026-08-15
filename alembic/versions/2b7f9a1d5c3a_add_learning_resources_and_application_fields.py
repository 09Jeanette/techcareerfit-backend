"""add learning_resources and application fields

Revision ID: 2b7f9a1d5c3a
Revises: e0c6344dca9b
Create Date: 2026-08-15 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2b7f9a1d5c3a'
down_revision: Union[str, Sequence[str], None] = 'e0c6344dca9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add learning_resources JSONB to ats_results
    op.add_column('ats_results', sa.Column('learning_resources', postgresql.JSONB(astext_type=sa.Text()), nullable=True))

    # Add richer tracking fields to applications
    op.add_column('applications', sa.Column('job_description', sa.Text(), nullable=True))
    op.add_column('applications', sa.Column('date_posted', sa.Date(), nullable=True))
    op.add_column('applications', sa.Column('cv_id', postgresql.UUID(), nullable=True))
    op.add_column('applications', sa.Column('ats_score', sa.Integer(), nullable=True))
    op.add_column('applications', sa.Column('comments', sa.Text(), nullable=True))

    # Create foreign key for cv_id -> cvs.id
    op.create_foreign_key('applications_cv_id_fkey', 'applications', 'cvs', ['cv_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop FK then columns on downgrade
    op.drop_constraint('applications_cv_id_fkey', 'applications', type_='foreignkey')
    op.drop_column('applications', 'comments')
    op.drop_column('applications', 'ats_score')
    op.drop_column('applications', 'cv_id')
    op.drop_column('applications', 'date_posted')
    op.drop_column('applications', 'job_description')

    op.drop_column('ats_results', 'learning_resources')
