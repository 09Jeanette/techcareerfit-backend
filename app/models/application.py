import uuid

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID

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
