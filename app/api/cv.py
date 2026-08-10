import uuid

from fastapi import APIRouter
from fastapi import File
from fastapi import UploadFile
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.storage import supabase
from app.core.security import get_current_user
from app.models.cv import CV
from app.models.user import User

router = APIRouter(
    prefix="/cv",
    tags=["CV"]
)


@router.post("/upload")
async def upload_cv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    allowed_extensions = ["pdf", "docx"]

    extension = file.filename.split(".")[-1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed"
        )

    unique_name = f"{uuid.uuid4()}.{extension}"

    file_content = await file.read()

    try:
        supabase.storage.from_("cvs").upload(
            path=unique_name,
            file=file_content,
            file_options={
                "content-type": file.content_type
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Storage upload failed: {str(e)}"
        )

    cv = CV(
        user_id=current_user.id,
        file_name=file.filename,
        file_url=unique_name
    )

    db.add(cv)
    db.commit()
    db.refresh(cv)

    return {
        "id": str(cv.id),
        "message": "CV uploaded successfully",
        "file_name": cv.file_name,
        "file_url": cv.file_url
    }


@router.get("/")
def get_all_cvs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cvs = db.query(CV).filter(CV.user_id == current_user.id).all()

    return cvs


@router.get("/{cv_id}")
def get_cv(
    cv_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cv = db.query(CV).filter(
        CV.id == cv_id,
        CV.user_id == current_user.id
    ).first()

    if not cv:
        raise HTTPException(
            status_code=404,
            detail="CV not found"
        )

    return cv


@router.delete("/{cv_id}")
def delete_cv(
    cv_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cv = db.query(CV).filter(
        CV.id == cv_id,
        CV.user_id == current_user.id
    ).first()

    if not cv:
        raise HTTPException(
            status_code=404,
            detail="CV not found"
        )

    try:
        supabase.storage.from_("cvs").remove(
            [cv.file_url]
        )
    except Exception:
        pass

    db.delete(cv)
    db.commit()

    return {
        "message": "CV deleted successfully"
    }