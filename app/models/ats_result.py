import uuid

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import Base


class ATSResult(Base):
    __tablename__ = "ats_results"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id")
    )

    cv_id = Column(
        UUID(as_uuid=True),
        ForeignKey("cvs.id")
    )

    job_id = Column(
        UUID(as_uuid=True),
        ForeignKey("job_descriptions.id")
    )

    score = Column(Integer)

    missing_skills = Column(JSONB)

    recommendations = Column(JSONB)
    
    # Learning resources mapped to missing skills (list of objects)
    learning_resources = Column(JSONB, nullable=True)