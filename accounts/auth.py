import bcrypt
import jwt

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session

from . import crud
from database.database import get_db
from settings import settings


oauth_scheme = OAuth2PasswordBearer(tokenUrl='accounts/token')


def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, settings.JWT_ALGORITHM)
        db_user = crud.get_user_by_email(db, payload.get('email'))
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return db_user


def pass_valid(password: str, password_hash: str) -> bool:
    if not bcrypt.checkpw(password.encode(), password_hash.encode()):
        return False
    return True