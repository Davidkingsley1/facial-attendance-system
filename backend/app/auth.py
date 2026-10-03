from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import create_access_token, get_current_user, verify_password
from app.database import SessionLocal
from app.models import AdminUser
from app.schemas import AdminLoginRequest, TokenResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: AdminLoginRequest):
    db: Session = SessionLocal()
    user = db.query(AdminUser).filter(AdminUser.username == payload.username).first()
    db.close()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    token = create_access_token({"sub": user.username, "role": user.role}, expires_delta=timedelta(days=1))
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def me(current_user: AdminUser = Depends(get_current_user)):
    return {"username": current_user.username, "role": current_user.role}
