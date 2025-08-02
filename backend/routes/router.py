from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import Student
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from backend.schemas import StudentResponse, StudentUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/students")
def add_student(name: str, grade: str, interests: str, age: int, db: Session = Depends(get_db)):
    student = Student(name=name, grade=grade, interests=interests, age=age)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@router.get("/students", response_model=List[StudentResponse])
def get_all_students(
    grade: Optional[str] = Query(None),
    min_age: Optional[int] = Query(None),
    max_age: Optional[int] = Query(None),
    sort_by: Optional[str] = Query(None, regex="^(name|age|grade)$"),
    order: Optional[str] = Query("asc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    query = db.query(Student)

    if grade:
        query = query.filter(Student.grade == grade)
    if min_age:
        query = query.filter(Student.age >= min_age)
    if max_age:
        query = query.filter(Student.age <= max_age)

    if sort_by:
        sort_column = getattr(Student, sort_by)
        if order == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)

    return query.all()

@router.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}

@router.put("/students/{student_id}")
def update_student(student_id: int, student_data: StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in student_data.dict(exclude_unset=True).items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return student
