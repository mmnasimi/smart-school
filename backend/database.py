from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from backend.models import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./school.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
async def get_user_db():
    db = SessionLocal()
    yield SQLAlchemyUserDatabase(db, User)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()