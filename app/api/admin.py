from fastapi import APIRouter, Depends, HTTPException, status
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

    users_count = db.query(func.count(User.id)).scalar()
    cvs_count = db.query(func.count(CV.id)).scalar()
    applications_count = db.query(func.count(Application.id)).scalar()

    avg_ats_score = db.query(func.avg(ATSResult.score)).scalar() or 0

    return {
        "users": int(users_count or 0),
        "cvs": int(cvs_count or 0),
        "applications": int(applications_count or 0),
        "average_ats_score": float(avg_ats_score)
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
