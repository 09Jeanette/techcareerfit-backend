
from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.user import User

from app.schemas.recommendation import (
    LearningRecommendationRequest,
    LearningResource
)

from app.services.recommendation_engine import (
    get_learning_recommendations
)


router = APIRouter(
    prefix="/recommendations",
    tags=["Learning Recommendations"]
)


@router.post(
    "/learning",
    response_model=list[LearningResource]
)
def get_recommendations(
    payload: LearningRecommendationRequest,
    current_user: User = Depends(get_current_user)
):

    return get_learning_recommendations(
        payload.missing_skills
    )

