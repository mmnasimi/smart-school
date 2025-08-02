from sqlalchemy.orm import mapped_column
from backend.base import Base
from sqlalchemy.orm import Mapped
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

class User(SQLAlchemyBaseUserTableUUID, Base):
    pass

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    grade: Mapped[str] = mapped_column(nullable=False)
    interests: Mapped[str] = mapped_column()
    age: Mapped[int] = mapped_column()