
from uuid import UUID
from typing import Optional, List

from pydantic import BaseModel


class SkillsGapAnalyzeRequest(BaseModel):
    cv_id: UUID
    roadmap: str


class SkillsGapResponse(BaseModel):
    id: UUID
    cv_id: UUID
    roadmap: str

    matched_skills: List[str]
    missing_skills: List[str]

    match_percentage: float

    recommended_learning: List[str]

    priority_level: str

    class Config:
        from_attributes = True
