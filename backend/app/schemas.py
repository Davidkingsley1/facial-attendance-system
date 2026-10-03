from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime, date


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class EmployeeCreate(BaseModel):
    employee_id: str
    full_name: str
    department: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None


class EmployeeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: str
    full_name: str
    department: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    role: Optional[str]
    image_path: Optional[str]
    created_at: Optional[datetime]


class AttendanceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: int
    employee_name: Optional[str] = None
    attendance_date: date
    clock_in: Optional[datetime]
    clock_out: Optional[datetime]
    status: Optional[str]
    remarks: Optional[str]
