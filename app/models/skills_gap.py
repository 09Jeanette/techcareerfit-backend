import uuid

from sqlalchemy import Column, String, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.core.database import Base


class SkillsGap(Base):
    __tablename__ = "skills_gaps"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    cv_id = Column(
        UUID(as_uuid=True),
        ForeignKey("cvs.id"),
        nullable=False
    )

    roadmap = Column(
        String,
        nullable=False
    )

    missing_skills = Column(
        JSON,
        nullable=False,
        default=list
    )

    recommended_learning = Column(
        JSON,
        nullable=False,
        default=list
    )

    priority_level = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )