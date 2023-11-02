from sqlalchemy.orm import Session

import models
import schemas
  

def create_user(db: Session, user: schemas.UserPost) -> models.User:
    db_user = models.User(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter_by(email=email).one()
