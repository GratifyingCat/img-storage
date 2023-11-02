from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from settings import settings


engine = create_engine(url=settings.DB_URL, echo=True)
session_local = sessionmaker(bind=engine)
Base = declarative_base()


def get_db() -> Session:
    db = session_local()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
    