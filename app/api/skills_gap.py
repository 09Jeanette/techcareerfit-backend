from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.core.database import get_db
from app.core.security import get_current_user

from app.models.user import User
from app.models.cv import CV
from app.models.skills_gap import SkillsGap

from app.schemas.skills_gap import (
    SkillsGapAnalyzeRequest,
    SkillsGapResponse
)

from app.services.skills_gap_engine import (
    analyze_against_roadmap
)


router = APIRouter(
    prefix="/skills-gap",
    tags=["Skills Gap"]
)


@router.post(
    "/analyze",
    response_model=SkillsGapResponse
)
def analyze_skills_gap(
    payload: SkillsGapAnalyzeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    cv = db.query(CV).filter(
        CV.id == payload.cv_id,
        CV.user_id == current_user.id
    ).first()

    if not cv:
        raise HTTPException(
            status_code=404,
            detail="CV not found"
        )

    if not cv.parsed_data:
        raise HTTPException(
            status_code=400,
            detail="CV has not been parsed yet"
        )

    cv_skills = cv.parsed_data.get("skills", [])

    if not cv_skills:
        raise HTTPException(
            status_code=400,
            detail="No skills were found in the parsed CV"
        )

    try:
        result_data = analyze_against_roadmap(
            cv_skills,
            payload.roadmap
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    gap = SkillsGap(
        id=uuid.uuid4(),
        user_id=current_user.id,
        cv_id=cv.id,
        roadmap=result_data["roadmap"],
        missing_skills=result_data["missing_skills"],
        recommended_learning=result_data["recommended_learning"],
        priority_level=result_data["priority_level"]
    )

    db.add(gap)
    db.commit()
    db.refresh(gap)

    return {
        "id": gap.id,
        "cv_id": gap.cv_id,
        "roadmap": gap.roadmap,
        "matched_skills": result_data["matched_skills"],
        "missing_skills": result_data["missing_skills"],
        "match_percentage": result_data["match_percentage"],
        "recommended_learning": result_data["recommended_learning"],
        "priority_level": result_data["priority_level"]
    }


@router.get(
    "/results",
    response_model=list[SkillsGapResponse]
)
def list_skills_gap_results(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return db.query(SkillsGap).filter(
        SkillsGap.user_id == current_user.id
    ).all()

