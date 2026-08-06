import uuid

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id")
    )

    title = Column(String)
    company = Column(String)
    description = Column(Text)