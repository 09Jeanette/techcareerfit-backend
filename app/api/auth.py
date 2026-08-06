from fastapi import APIRouter
from app.schemas.auth import UserRegister, UserLogin

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.get("/")
def auth_status():
    return {
        "message": "Auth module running"
    }


@router.post("/register")
def register(user: UserRegister):
    return {
        "message": "User registered successfully",
        "user": {
            "full_name": user.full_name,
            "email": user.email
        }
    }


@router.post("/login")
def login(user: UserLogin):
    return {
        "message": "Login successful",
        "email": user.email
    }