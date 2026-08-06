from fastapi import APIRouter

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.get("/")
def jobs_status():
    return {
        "message": "Jobs endpoint"
    }