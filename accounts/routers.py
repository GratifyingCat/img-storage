import bcrypt
import jwt

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import EmailStr

from . import crud
from . import schemas
from database.database import get_db

from .auth import pass_valid, get_current_user
from settings import settings


router = APIRouter(
    prefix='/accounts',
    tags=['accounts']
)


@router.post('/token')
def generate_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, form_data.username)
    if not db_user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    if not pass_valid(form_data.password, db_user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    user = {
        'email': db_user.email,
        'exp': settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    }
    token = jwt.encode(user, settings.JWT_SECRET, settings.JWT_ALGORITHM)
    return {'access_token': token, 'token_type': 'bearer'}


@router.post('/create')
def create_user(email: EmailStr, password: str, db: Session = Depends(get_db)):
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user_db = schemas.UserPost(
        email=email,
        password_hash=password_hash
    )
    return crud.create_user(db, user_db)


@router.get('/user')
def get_user(email: EmailStr, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return crud.get_user_by_email(db, email)


@router.get('/me')
def login_user(db_user: schemas.User = Depends(get_current_user)):
    return db_user
