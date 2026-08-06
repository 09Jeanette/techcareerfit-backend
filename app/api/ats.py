from fastapi import APIRouter

router = APIRouter(
    prefix="/ats",
    tags=["ATS"]
)


@router.get("/")
def ats_status():
    return {
        "message": "ATS engine endpoint"
    }