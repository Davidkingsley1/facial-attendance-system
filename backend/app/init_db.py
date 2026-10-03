from app.config import settings
from app.database import SessionLocal
from app.models import AdminUser
from app.auth import hash_password


def create_default_admin():
    db = SessionLocal()
    exists = db.query(AdminUser).filter(AdminUser.username == settings.ADMIN_USERNAME).first()
    if not exists:
        db.add(
            AdminUser(
                username=settings.ADMIN_USERNAME,
                password_hash=hash_password(settings.ADMIN_PASSWORD),
                role="admin",
            )
        )
        db.commit()
    db.close()
