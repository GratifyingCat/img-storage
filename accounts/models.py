from database.database import Base

from sqlalchemy import Column, String, Integer


class User(Base):
    __tablename__ = 'users'
    
    id: int = Column(Integer(), primary_key=True, unique=True, autoincrement=True)
    email: str = Column(String(), unique=True)
    password_hash: str = Column(String())
    