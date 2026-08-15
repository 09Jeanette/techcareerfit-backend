from uuid import UUID
from datetime import date
from typing import Optional

from pydantic import BaseModel


class ApplicationCreate(BaseModel):
    company: str
    position: str
    status: Optional[str] = "applied"
    applied_date: Optional[date] = None

    # Optional richer tracking
    job_description: Optional[str] = None
    date_posted: Optional[date] = None
    cv_id: Optional[UUID] = None
    ats_score: Optional[int] = None
    comments: Optional[str] = None
    job_link: Optional[str] = None
    application_email: Optional[str] = None
    application_subject: Optional[str] = None


class ApplicationResponse(BaseModel):
    id: UUID
    company: str
    position: str
    status: Optional[str]
    applied_date: Optional[date]

    job_description: Optional[str]
    date_posted: Optional[date]
    cv_id: Optional[UUID]
    ats_score: Optional[int]
    comments: Optional[str]
    job_link: Optional[str]
    application_email: Optional[str]
    application_subject: Optional[str]

    class Config:
        from_attributes = True
