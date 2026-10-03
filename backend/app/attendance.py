from datetime import date, datetime, time
from typing import Dict, Any

import face_recognition
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Attendance, Employee, FaceEmbedding

router = APIRouter(prefix="/api", tags=["attendance"])


def _late_status(clock_in_time: datetime) -> str:
    threshold = time(9, 0)
    if clock_in_time.time() > threshold:
        return "late"
    return "present"


@router.post("/attendance/recognize")
async def recognize_employee(image: UploadFile = File(...)):
    db: Session = SessionLocal()
    embeddings = db.query(FaceEmbedding).all()
    if not embeddings:
        db.close()
        raise HTTPException(status_code=404, detail="No registered employees available for recognition")

    content = await image.read()
    temp_path = f"/tmp/{image.filename or 'capture.jpg'}"
    with open(temp_path, "wb") as f:
        f.write(content)

    try:
        image_array = face_recognition.load_image_file(temp_path)
        face_locations = face_recognition.face_locations(image_array)
        if not face_locations:
            raise HTTPException(status_code=400, detail="No face detected in the uploaded image")

        face_encoding = face_recognition.face_encodings(image_array, face_locations)[0]
        known_encodings = [embedding.face_encoding for embedding in embeddings]
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.42)

        if not any(matches):
            return {"matched": False, "message": "Employee not recognized"}

        matched_index = matches.index(True)
        matched_embedding = embeddings[matched_index]
        employee = db.query(Employee).filter(Employee.id == matched_embedding.employee_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee record not found")

        today = date.today()
        attendance = db.query(Attendance).filter(
            Attendance.employee_id == employee.id,
            Attendance.attendance_date == today,
        ).first()

        now = datetime.utcnow()

        if attendance is None:
            attendance = Attendance(
                employee_id=employee.id,
                attendance_date=today,
                clock_in=now,
                clock_out=None,
                status="present",
                remarks="Clock-in recorded",
            )
            db.add(attendance)
            db.commit()
            db.refresh(attendance)
            return {
                "matched": True,
                "employee_id": employee.employee_id,
                "employee_name": employee.full_name,
                "status": _late_status(now),
                "message": "Clock-in recorded successfully",
                "clock_in": attendance.clock_in.isoformat() if attendance.clock_in else None,
            }

        if attendance.clock_in and attendance.clock_out is None:
            attendance.clock_out = now
            attendance.status = "present"
            attendance.remarks = "Clock-out recorded"
            db.commit()
            db.refresh(attendance)
            return {
                "matched": True,
                "employee_id": employee.employee_id,
                "employee_name": employee.full_name,
                "status": "present",
                "message": "Clock-out recorded successfully",
                "clock_out": attendance.clock_out.isoformat() if attendance.clock_out else None,
            }

        return {
            "matched": True,
            "employee_id": employee.employee_id,
            "employee_name": employee.full_name,
            "status": attendance.status,
            "message": "Attendance already recorded for today",
        }
    finally:
        db.close()


@router.get("/attendance/report")
def attendance_report(date_value: str = None):
    db: Session = SessionLocal()
    target_date = date.fromisoformat(date_value) if date_value else date.today()
    employee_rows = db.query(Employee).all()
    list_data = []

    for employee in employee_rows:
        attendance = db.query(Attendance).filter(
            Attendance.employee_id == employee.id,
            Attendance.attendance_date == target_date,
        ).first()
        list_data.append({
            "employee_id": employee.employee_id,
            "employee_name": employee.full_name,
            "department": employee.department,
            "status": attendance.status if attendance else "absent",
            "clock_in": attendance.clock_in.isoformat() if attendance and attendance.clock_in else None,
            "clock_out": attendance.clock_out.isoformat() if attendance and attendance.clock_out else None,
        })

    db.close()
    return {"date": target_date.isoformat(), "records": list_data}


@router.get("/attendance/today")
def attendance_today():
    return attendance_report(date_value=date.today().isoformat())
