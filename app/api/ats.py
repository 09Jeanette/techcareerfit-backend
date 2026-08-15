from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.cv import CV
from app.models.job import JobDescription
from app.models.ats_result import ATSResult
from app.schemas.ats import (
    JobDescriptionCreate,
    JobDescriptionResponse,
    ATSAnalyzeRequest,
    ATSResultResponse,
)
from app.services.ats_engine import extract_job_skills, score_cv_against_job
from app.services.recommendation_engine import get_learning_recommendations

router = APIRouter(
    prefix="/ats",
    tags=["ATS"]
)


@router.get("/")
def ats_status():
    return {
        "message": "ATS engine endpoint"
    }


@router.post("/jobs", response_model=JobDescriptionResponse)
def create_job_description(
    payload: JobDescriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = JobDescription(
        user_id=current_user.id,
        title=payload.title,
        company=payload.company,
        description=payload.description
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


@router.get("/jobs", response_model=list[JobDescriptionResponse])
def list_job_descriptions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(JobDescription).filter(
        JobDescription.user_id == current_user.id
    ).all()


@router.post("/analyze", response_model=ATSResultResponse)
def analyze_cv(
    payload: ATSAnalyzeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cv = db.query(CV).filter(
        CV.id == payload.cv_id,
        CV.user_id == current_user.id
    ).first()

    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")

    if not cv.parsed_data:
        raise HTTPException(
            status_code=400,
            detail="CV has not been parsed yet — call POST /cv/{cv_id}/parse first"
        )

    job = db.query(JobDescription).filter(
        JobDescription.id == payload.job_id,
        JobDescription.user_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job description not found")

    cv_skills = cv.parsed_data.get("skills", [])
    job_skills = extract_job_skills(job.description)  # computed fresh each time, not stored

    result_data = score_cv_against_job(cv_skills, job_skills)

    # Map missing skills to learning resources
    learning_resources = get_learning_recommendations(result_data.get("missing_skills", []))
    result_data["learning_resources"] = learning_resources

    ats_result = ATSResult(
        user_id=current_user.id,
        cv_id=cv.id,
        job_id=job.id,
        score=result_data["score"],
        missing_skills=result_data["missing_skills"],
        recommendations=result_data["recommendations"],
        learning_resources=result_data.get("learning_resources")
    )

    db.add(ats_result)
    db.commit()
    db.refresh(ats_result)

    return ats_result


@router.get("/results", response_model=list[ATSResultResponse])
def list_ats_results(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(ATSResult).filter(
        ATSResult.user_id == current_user.id
    ).all()