from typing import Optional

from pydantic import BaseModel, EmailStr
from uuid import UUID

class StudentCreate(BaseModel):
    name: str
    grade: str
    interests: str
    age: int

class StudentResponse(BaseModel):
    id: int
    name: str
    grade: str
    interests: str
    age: int

    class Config:
        from_attributes = True  # به جای orm_mode

class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool
    is_superuser: bool
    # می‌تونی فیلدهای دیگه هم اضافه کنی

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class StudentUpdate(BaseModel):
    name: Optional[str]
    grade: Optional[str]
    interests: Optional[str]
    age: Optional[int]
