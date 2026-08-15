from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.ats_result import ATSResult
from app.models.user import User


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/")
def reports_status():
    return {
        "message": "Reports endpoint"
    }


@router.get("/{report_id}/download")
def download_report(report_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    report = db.query(ATSResult).filter(ATSResult.id == report_id).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # Allow owner or admin
    if str(report.user_id) != str(current_user.id) and getattr(current_user, "role", "job_seeker") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to download this report")

    payload = {
        "id": str(report.id),
        "user_id": str(report.user_id) if report.user_id else None,
        "cv_id": str(report.cv_id) if report.cv_id else None,
        "job_id": str(report.job_id) if report.job_id else None,
        "score": report.score,
        "missing_skills": report.missing_skills,
        "recommendations": report.recommendations,
        "learning_resources": report.learning_resources
    }

    return JSONResponse(content=payload, media_type="application/json", headers={"Content-Disposition": f"attachment; filename=report_{report_id}.json"})