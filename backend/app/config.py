from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/attendance_db")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "supersecretkey123")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", str(BASE_DIR / "backend" / "uploads"))

settings = Settings()
