from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator  

DATABASE_URL = "sqlite:///./students.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    roll = Column(String, unique=True)
    marks = Column(Integer)
    total = Column(Integer)

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def get_db() -> Generator[Session, None, None]:  
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=RedirectResponse)
async def read_root():
    return RedirectResponse(url="/students")

@app.get("/students", response_class=templates.TemplateResponse)
async def get_students(request: Request, db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return templates.TemplateResponse("students.html", {"request": request, "students": students})

@app.post("/students", response_class=RedirectResponse)
async def create_student(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    new_student = Student(
        name=form_data.get("name"),
        roll=form_data.get("roll"),
        marks=int(form_data.get("marks")),
        total=int(form_data.get("total"))
    )
    db.add(new_student)
    db.commit()
    return RedirectResponse(url="/students", status_code=303)
