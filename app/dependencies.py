from sqlalchemy import select

from app.database import DbSession
from app.models import User

DEV_EMAIL = "dev@citesem.local"


def get_current_user(db: DbSession) -> User:
    """TEMPORARY stub. Replaced by real JWT auth on 20 Oct."""
    user = db.scalar(select(User).where(User.email == DEV_EMAIL))
    if user is None:
        user = User(email=DEV_EMAIL, password_hash="not-a-real-hash")
        db.add(user)
        db.commit()
        db.refresh(user)
    return user