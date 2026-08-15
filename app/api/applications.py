from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
import uuid

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.application import Application
from app.models.user import User

from app.schemas.application import (
    ApplicationCreate,
    ApplicationResponse
)

router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


@router.post("/", response_model=ApplicationResponse)
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    app_entry = Application(
        id=uuid.uuid4(),
        user_id=current_user.id,
        company=payload.company,
        position=payload.position,
        status=payload.status,
        applied_date=payload.applied_date or date.today(),
        job_description=payload.job_description,
        date_posted=payload.date_posted,
        cv_id=payload.cv_id,
        ats_score=payload.ats_score,
        comments=payload.comments,
        job_link=payload.job_link,
        application_email=payload.application_email,
        application_subject=payload.application_subject,
    )

    db.add(app_entry)
    db.commit()
    db.refresh(app_entry)

    return app_entry


@router.get("/", response_model=list[ApplicationResponse])
def list_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Application).filter(Application.user_id == current_user.id).all()


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(
    application_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    app_entry = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not app_entry:
        raise HTTPException(status_code=404, detail="Application not found")

    return app_entry


@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: str,
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    app_entry = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not app_entry:
        raise HTTPException(status_code=404, detail="Application not found")

    app_entry.company = payload.company
    app_entry.position = payload.position
    app_entry.status = payload.status
    app_entry.applied_date = payload.applied_date or app_entry.applied_date

    app_entry.job_description = payload.job_description
    app_entry.date_posted = payload.date_posted or app_entry.date_posted
    app_entry.cv_id = payload.cv_id or app_entry.cv_id
    app_entry.ats_score = payload.ats_score or app_entry.ats_score
    app_entry.comments = payload.comments or app_entry.comments
    app_entry.job_link = payload.job_link or app_entry.job_link
    app_entry.application_email = payload.application_email or app_entry.application_email
    app_entry.application_subject = payload.application_subject or app_entry.application_subject

    db.commit()
    db.refresh(app_entry)

    return app_entry


@router.delete("/{application_id}")
def delete_application(
    application_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    app_entry = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not app_entry:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(app_entry)
    db.commit()

    return {"message": "Application deleted successfully"}
