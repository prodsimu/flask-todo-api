from sqlalchemy import select

from app.database.database import db
from app.models import User, UserRole
from app.services import UserService


def seed_admin():
    existing_admin = db.session.execute(
        select(User).filter_by(role=UserRole.ADMIN.value)
    ).scalar()

    if existing_admin:
        return False

    admin = UserService.create_user(
        name="Admin", username="admin", password="admin123456"
    )

    admin.role = UserRole.ADMIN.value
    db.session.commit()

    return True
