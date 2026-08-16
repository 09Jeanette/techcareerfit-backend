from collections import Counter
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.security import hash_password
from app.models.user import User
from app.models.cv import CV
from app.models.application import Application
from app.models.ats_result import ATSResult
from app.models.job import JobDescription
from app.core.storage import supabase
from fastapi.responses import JSONResponse
from fastapi import Path
from fastapi.responses import StreamingResponse
import io

from app.schemas.auth import UserRegister


class ApplicationStatusUpdate(BaseModel):
    status: str


def build_monthly_trend_from_dates(dates, months=6):
    month_counts = Counter()
    for value in dates:
        if value is None:
            continue
        month_counts[value.strftime("%Y-%m")] += 1

    current_month = date.today().replace(day=1)
    trend = []
    for offset in range(months - 1, -1, -1):
        month_cursor = current_month
        if offset > 0:
            year = current_month.year
            month = current_month.month - offset
            while month <= 0:
                month += 12
                year -= 1
            while month > 12:
                month -= 12
                year += 1
            month_cursor = date(year, month, 1)
        label = month_cursor.strftime("%Y-%m")
        trend.append({
            "label": label,
            "value": month_counts.get(label, 0)
        })

    return trend


def build_distribution_from_values(values, buckets):
    counts = {label: 0 for label in buckets}
    for value in values:
        if value is None:
            continue
        for label, range_tuple in buckets.items():
            lower, upper = range_tuple
            if value >= lower and value <= upper:
                counts[label] += 1
                break
    return [{"label": label, "value": count} for label, count in counts.items()]


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/")
def stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Only allow admin roles
    if getattr(current_user, "role", "job_seeker") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )

    users_count = db.query(func.count(User.id)).scalar() or 0
    cvs_count = db.query(func.count(CV.id)).scalar() or 0
    applications_count = db.query(func.count(Application.id)).scalar() or 0
    avg_ats_score = db.query(func.avg(ATSResult.score)).scalar() or 0

    role_counts = db.query(User.role, func.count(User.id)).group_by(User.role).all()
    status_counts = db.query(Application.status, func.count(Application.id)).group_by(Application.status).all()
    application_dates = [app.applied_date for app in db.query(Application).all()]
    ats_scores = [result.score for result in db.query(ATSResult).all() if result.score is not None]

    users_by_role = [{"label": role or "unknown", "value": int(value)} for role, value in role_counts]
    applications_by_status = [{"label": status or "unknown", "value": int(value)} for status, value in status_counts]
    applications_by_month = build_monthly_trend_from_dates(application_dates, months=6)
    ats_score_distribution = build_distribution_from_values(
        ats_scores,
        {
            "0-49": (0, 49),
            "50-69": (50, 69),
            "70-89": (70, 89),
            "90-100": (90, 100),
        }
    )

    jobs_by_company = db.query(Application.company, func.count(Application.id)).group_by(Application.company).all()
    jobs_by_company = [{"label": company or "unknown", "value": int(value)} for company, value in jobs_by_company]

    summary = {
        "users": int(users_count),
        "cvs": int(cvs_count),
        "applications": int(applications_count),
        "average_ats_score": float(avg_ats_score),
        "admins": int(db.query(func.count(User.id)).filter(User.role == "admin").scalar() or 0),
        "job_seekers": int(db.query(func.count(User.id)).filter(User.role == "job_seeker").scalar() or 0),
        "suspended_users": int(db.query(func.count(User.id)).filter(User.suspended.is_(True)).scalar() or 0),
        "active_applications": int(db.query(func.count(Application.id)).filter(Application.status.in_(["applied", "interview", "offer"])).scalar() or 0),
    }

    return {
        "users": int(users_count),
        "cvs": int(cvs_count),
        "applications": int(applications_count),
        "average_ats_score": float(avg_ats_score),
        "summary": summary,
        "charts": {
            "users_by_role": users_by_role,
            "applications_by_status": applications_by_status,
            "applications_by_month": applications_by_month,
            "ats_score_distribution": ats_score_distribution,
            "jobs_by_company": jobs_by_company,
        },
    }


@router.get("/users/")
def list_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "role", "job_seeker") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    users = db.query(User).all()
    return users


@router.get("/users/{user_id}")
def get_user(user_id: str = Path(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "role", "job_seeker") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}")
def delete_user(user_id: str = Path(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "role", "job_seeker") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}


@router.post("/users/")
def create_user(payload: UserRegister, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "role", "job_seeker") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hash_password(payload.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created", "id": str(new_user.id), "email": new_user.email}


@router.post("/users/{user_id}/suspend")
def suspend_user(user_id: str = Path(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "role", "job_seeker") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.suspended = True
    db.commit()
    return {"message": f"User {user.email} suspended"}


@router.post("/users/{user_id}/unsuspend")
def unsuspend_user(user_id: str = Path(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "role", "job_seeker") != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.suspended = False
    db.commit()
    return {"message": f"User {user.email} unsuspended"}


@router.post("/users/{user_id}/promote")
def promote_user(user_id: str = Path(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Only admins can promote
    if getattr(current_user, "role", "job_seeker") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = "admin"
    db.commit()
    db.refresh(user)

    return {"message": f"User {user.email} promoted to admin"}


@router.get("/jobs/")
def list_jobs(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "role", "job_seeker") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    jobs = db.query(JobDescription).all()
    return jobs


@router.delete("/jobs/{job_id}")
def delete_job(job_id: str = Path(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "role", "job_seeker") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    db.delete(job)
    db.commit()
    return {"message": "Job deleted"}


@router.get("/cvs/")
def list_all_cvs(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "role", "job_seeker") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    cvs = db.query(CV).all()
    return cvs


@router.get("/cvs/{cv_id}/parsed")
def admin_get_parsed_cv(cv_id: str = Path(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "role", "job_seeker") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    cv = db.query(CV).filter(CV.id == cv_id).first()
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")

    return {
        "id": str(cv.id),
        "file_name": cv.file_name,
        "parsed_at": cv.parsed_at,
        "parsed_data": cv.parsed_data
    }


@router.get("/cvs/{cv_id}/download")
def admin_download_cv(cv_id: str = Path(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "role", "job_seeker") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    cv = db.query(CV).filter(CV.id == cv_id).first()
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")

    try:
        file_bytes = supabase.storage.from_("cvs").download(cv.file_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download file from storage: {str(e)}")

    return StreamingResponse(io.BytesIO(file_bytes), media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={cv.file_name}"})


@router.delete("/cvs/{cv_id}")
def delete_any_cv(cv_id: str = Path(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "role", "job_seeker") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    cv = db.query(CV).filter(CV.id == cv_id).first()
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")

    try:
        supabase.storage.from_("cvs").remove([cv.file_url])
    except Exception:
        pass

    db.delete(cv)
    db.commit()

    return {"message": "CV deleted"}


@router.get("/applications/")
def list_all_applications(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "role", "job_seeker") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    apps = db.query(Application).all()
    return [
        {
            "id": str(app.id),
            "user_id": str(app.user_id) if app.user_id else None,
            "company": app.company,
            "position": app.position,
            "status": app.status,
            "applied_date": app.applied_date.isoformat() if app.applied_date else None,
            "job_description": app.job_description,
            "date_posted": app.date_posted.isoformat() if app.date_posted else None,
            "cv_id": str(app.cv_id) if app.cv_id else None,
            "ats_score": app.ats_score,
            "comments": app.comments,
            "job_link": app.job_link,
            "application_email": app.application_email,
            "application_subject": app.application_subject,
        }
        for app in apps
    ]


@router.get("/applications/{application_id}")
def get_application_admin(application_id: str = Path(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "role", "job_seeker") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    return {
        "id": str(app.id),
        "user_id": str(app.user_id) if app.user_id else None,
        "company": app.company,
        "position": app.position,
        "status": app.status,
        "applied_date": app.applied_date.isoformat() if app.applied_date else None,
        "job_description": app.job_description,
        "date_posted": app.date_posted.isoformat() if app.date_posted else None,
        "cv_id": str(app.cv_id) if app.cv_id else None,
        "ats_score": app.ats_score,
        "comments": app.comments,
        "job_link": app.job_link,
        "application_email": app.application_email,
        "application_subject": app.application_subject,
    }


@router.patch("/applications/{application_id}/status")
def update_application_status(application_id: str = Path(...), payload: ApplicationStatusUpdate = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "role", "job_seeker") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    if payload is None:
        raise HTTPException(status_code=400, detail="Status payload is required")

    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    app.status = payload.status
    db.commit()
    db.refresh(app)

    return {"message": "Application status updated", "status": app.status}


@router.delete("/applications/{application_id}")
def delete_application_admin(application_id: str = Path(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "role", "job_seeker") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(app)
    db.commit()
    return {"message": "Application deleted"}


@router.get("/reports/")
def list_reports(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "role", "job_seeker") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    reports = db.query(ATSResult).all()
    return reports


@router.get("/reports/{report_id}")
def get_report(report_id: str = Path(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "role", "job_seeker") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    report = db.query(ATSResult).filter(ATSResult.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.delete("/reports/{report_id}")
def delete_report(report_id: str = Path(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if getattr(current_user, "role", "job_seeker") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

    report = db.query(ATSResult).filter(ATSResult.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    db.delete(report)
    db.commit()
    return {"message": "Report deleted"}
