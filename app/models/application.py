import uuid

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Integer
from sqlalchemy import Text

from app.core.database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id")
    )

    company = Column(String)

    position = Column(String)

    status = Column(String)

    applied_date = Column(Date)
    
    # Optional richer tracking fields
    job_description = Column(Text, nullable=True)

    date_posted = Column(Date, nullable=True)

    cv_id = Column(
        UUID(as_uuid=True),
        ForeignKey("cvs.id"),
        nullable=True
    )

    ats_score = Column(Integer, nullable=True)

    comments = Column(Text, nullable=True)

    # Link to the job posting (URL) or application portal
    job_link = Column(String, nullable=True)

    # If applied via email, store email address and subject line
    application_email = Column(String, nullable=True)
    application_subject = Column(String, nullable=True)
