from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.models import Student
from backend.schemas import StudentCreate, StudentResponse
from backend.database import get_db

router = APIRouter()

@router.post("/students", response_model=StudentResponse)
def add_student(student_data: StudentCreate, db: Session = Depends(get_db)):
    student = Student(**student_data.dict())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student