from fastapi import APIRouter

router = APIRouter(
    prefix="/cv",
    tags=["CV"]
)


@router.get("/")
def cv_status():
    return {
        "message": "CV endpoint"
    }