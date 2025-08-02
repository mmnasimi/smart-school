from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from backend.database import get_db
from backend.models import Student
from sqlalchemy.orm import Session
from backend.auth.routes import router as auth_router
from fastapi.staticfiles import StaticFiles
from fastapi_users import FastAPIUsers
# from fastapi_users.models import BaseUserDB
from fastapi import Depends, Request
from fastapi_users import FastAPIUsers


app = FastAPI()
app.include_router(auth_router)
templates = Jinja2Templates(directory="backend/templates")

app.mount("/static", StaticFiles(directory="backend/static"), name="static")

students_db = [
    {"name": "محمد", "grade": "ششم", "age": 12},
    {"name": "زهرا", "grade": "هفتم", "age": 13},
]

@app.get("/students/view", response_class=HTMLResponse)
def view_students(request: Request):
    return templates.TemplateResponse("students.html", {"request": request, "students": students_db})
# app.include_router(router)

@app.post("/students/add")
def add_student(name: str = Form(...), grade: str = Form(...), age: int = Form(...)):
    new_student = {"name": name, "grade": grade, "age": age}
    students_db.append(new_student)
    return RedirectResponse(url="/students/view", status_code=303)

@app.get("/students/search", response_class=HTMLResponse)
def search_students(request: Request, q: str = ""):
    filtered = [s for s in students_db if q in s["name"] or q in s["grade"]]
    return templates.TemplateResponse("students.html", {"request": request, "students": filtered})

@app.post("/students/delete")
def delete_student(name: str = Form(...)):
    global students_db
    students_db = [s for s in students_db if s["name"] != name]
    return RedirectResponse(url="/students/view", status_code=303)

@app.get("/")
def landing_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/create-student")
def create_student(
    name: str = Form(...),
    grade: str = Form(...),
    interests: str = Form(...),
    age: int = Form(...),
    db: Session = Depends(get_db)
):
    student = Student(name=name, grade=grade, interests=interests, age=age)
    db.add(student)
    db.commit()
    db.refresh(student)
    return {"message": "دانش‌آموز با موفقیت ثبت شد!", "student_id": student.id}


@app.get("/create-student-form", response_class=HTMLResponse)
def show_student_form(request: Request):
    return templates.TemplateResponse("create_student.html", {"request": request})

@app.get("/students", response_class=HTMLResponse)
def show_students(request: Request):
    return templates.TemplateResponse("students.html", {
        "request": request,
        "students": students_db  # یا هر لیست دیگری
    })

@app.get("/students/edit/{name}", response_class=HTMLResponse)
def edit_student_form(request: Request, name: str):
    student = next((s for s in students_db if s["name"] == name), None)
    return templates.TemplateResponse("edit_student.html", {
        "request": request,
        "student": student
    })

@app.post("/students/update")
def update_student(original_name: str = Form(...), name: str = Form(...), grade: str = Form(...), interests: str = Form(...), age: int = Form(...)):
    for student in students_db:
        if student["name"] == original_name:
            student.update({"name": name, "grade": grade, "interests": interests, "age": age})
    return RedirectResponse("/students", status_code=303)


@app.get("/register-form")
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login-form")
def get_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# @app.get("/dashboard")
# async def dashboard(request: Request, user: UserRead = Depends(current_active_user)):
#     return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})
