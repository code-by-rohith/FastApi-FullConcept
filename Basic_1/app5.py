from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
    name: str
    roll_no: int

students = [
    Student(name="Alice", roll_no=1),
    Student(name="Bob", roll_no=2),
    Student(name="Charlie", roll_no=3)
]

@app.get('/get/{roll_no}', response_model=Student)
def get_student(roll_no: int):
    for student in students:
        if student.roll_no == roll_no:
            return student
    raise HTTPException(status_code=404, detail="Student not found")


