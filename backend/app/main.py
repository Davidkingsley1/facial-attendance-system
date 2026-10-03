import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.auth import create_default_admin
from app.database import Base, SessionLocal, engine
from app import models
from app.attendance import router as attendance_router
from app.auth import router as auth_router
from app.employees import router as employees_router

BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATIC_DIR = BASE_DIR / "frontend" / "static"

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Facial Attendance System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(employees_router)
app.include_router(attendance_router)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.on_event("startup")
def startup_event():
    create_default_admin()


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")
