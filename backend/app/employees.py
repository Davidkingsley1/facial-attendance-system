import os
import json
from pathlib import Path
from datetime import date, datetime
from typing import List

import face_recognition
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.auth import get_current_user
from app.database import SessionLocal
from app.models import Employee, FaceEmbedding, Attendance
from app.schemas import EmployeeCreate, EmployeeOut

router = APIRouter(prefix="/api", tags=["employees"])
UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/employees", response_model=list[EmployeeOut])
def list_employees(current_user: dict = Depends(get_current_user)):
    db: Session = SessionLocal()
    employees = db.query(Employee).order_by(Employee.id.asc()).all()
    db.close()
    return employees


@router.post("/employees", response_model=EmployeeOut)
async def create_employee(
    employee_id: str = Form(...),
    full_name: str = Form(...),
    department: str = Form(None),
    phone: str = Form(None),
    email: str = Form(None),
    role: str = Form(None),
    image: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    db: Session = SessionLocal()
    if db.query(Employee).filter(Employee.employee_id == employee_id).first():
        db.close()
        raise HTTPException(status_code=400, detail="Employee ID already exists")

    filename = f"{employee_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{image.filename}"
    file_path = UPLOAD_DIR / filename
    contents = await image.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    image_array = face_recognition.load_image_file(file_path)
    face_locations = face_recognition.face_locations(image_array)
    if not face_locations:
        os.remove(file_path)
        db.close()
        raise HTTPException(status_code=400, detail="No face detected in the uploaded image")

    face_encoding = face_recognition.face_encodings(image_array, face_locations)[0]

    employee = Employee(
        employee_id=employee_id,
        full_name=full_name,
        department=department,
        phone=phone,
        email=email,
        role=role,
        image_path=str(file_path),
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)

    db.add(FaceEmbedding(employee_id=employee.id, face_encoding=face_encoding.tolist()))
    db.commit()

    employee.image_path = str(file_path)
    db.commit()
    db.refresh(employee)
    db.close()

    return employee
