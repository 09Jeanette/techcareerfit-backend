from fastapi import FastAPI

from app.api import auth
from app.api import users
from app.api import cv
from app.api import ats
from app.api import jobs
from app.api import reports

from app.core.database import Base
from app.core.database import engine

from app.models.user import User
from app.models.cv import CV
from app.models.job import JobDescription
from app.models.application import Application
from app.models.ats_result import ATSResult

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TechCareerFit API"
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(cv.router)
app.include_router(ats.router)
app.include_router(jobs.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to TechCareerFit API"
    }