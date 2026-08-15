
from typing import List

from pydantic import BaseModel


class LearningRecommendationRequest(BaseModel):
    missing_skills: List[str]


class LearningResource(BaseModel):
    skill: str
    title: str
    provider: str
    url: str
    type: str
    level: str

