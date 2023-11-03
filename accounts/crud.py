from sqlalchemy.orm import Session

from . import models
from . import schemas


def create_user(db: Session, user: schemas.UserPost) -> models.User:
    db_user = models.User(
        email=user.email,
        password_hash=user.password_hash
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()
