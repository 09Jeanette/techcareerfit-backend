from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth
from app.api import users
from app.api import cv
from app.api import ats
from app.api import jobs
from app.api import reports
from app.api import skills_gap

from app.api.recommendations import router as recommendations_router
from app.api.applications import router as applications_router
from app.api.admin import router as admin_router

from app.core.database import Base
from app.core.database import engine

# Import models so SQLAlchemy registers them
from app.models.user import User
from app.models.cv import CV
from app.models.job import JobDescription
from app.models.application import Application
from app.models.ats_result import ATSResult
from app.models.skills_gap import SkillsGap


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="TechCareerFit API"
)

# CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Authentication
app.include_router(auth.router)

# Users
app.include_router(users.router)

# CV
app.include_router(cv.router)

# ATS
app.include_router(ats.router)

# Jobs
app.include_router(jobs.router)

# Reports
app.include_router(reports.router)

# Skills Gap
app.include_router(skills_gap.router)

# Learning Recommendations
app.include_router(recommendations_router)

# Applications
app.include_router(applications_router)

# Admin
app.include_router(admin_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to TechCareerFit API"
    }