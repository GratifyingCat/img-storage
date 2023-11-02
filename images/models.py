from sqlalchemy import (Column, 
                        Integer,
                        String)

from database.database import Base


class Image(Base):
    __tablename__ = 'images'

    id: int = Column(Integer(), primary_key=True, autoincrement=True, unique=True)
    path: str = Column(String())
    