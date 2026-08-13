from uuid import UUID
from typing import Optional

from pydantic import BaseModel


class JobDescriptionCreate(BaseModel):
    title: str
    company: Optional[str] = None
    description: str


class JobDescriptionResponse(BaseModel):
    id: UUID
    title: str
    company: Optional[str]
    description: str

    class Config:
        from_attributes = True


class ATSAnalyzeRequest(BaseModel):
    cv_id: UUID
    job_id: UUID


class ATSResultResponse(BaseModel):
    id: UUID
    cv_id: UUID
    job_id: UUID
    score: int
    missing_skills: list[str]
    recommendations: list[str]

    class Config:
        from_attributes = True