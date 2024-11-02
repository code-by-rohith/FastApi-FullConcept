from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from random import randrange
from typing import Optional, List

app = FastAPI()

# Class for Personal Details
class PersonalDetails(BaseModel):
    name: str 
    age: int 
    gender: Optional[str] = None 
    email: EmailStr 
    phone: str 
    address: str

class SchoolDetails(BaseModel):
    roll: int  
    department: str  
    year_of_study: int 
    grade: str 
    gpa: Optional[float] = None 

class StudentDetails(PersonalDetails, SchoolDetails):
    pass

my_post: List[dict] = [{
    "name": "hari", "age": 20, "gender": "Male", "email": "hari@example.com",
    "phone": "+1234567890", "address": "123 Main St", "roll": 36,
    "department": "Computer Science", "year_of_study": 3, "grade": "A", "gpa": 3.8, "id": 1
}]

def helper_delete(id):
    for i, data in enumerate(my_post):
        if data['id'] == id:
            return i
    return None

@app.get('/getall')
def all_get():
    return my_post

@app.post('/post', status_code=status.HTTP_201_CREATED)
def create_student(details: StudentDetails):
    student = details.dict()
    for data in my_post:
        if student['roll'] == data['roll']:
            return {"message": "Student with this roll number already exists"}
    student['id'] = randrange(1, 100000000)
    my_post.append(student)
    return my_post

@app.get('/get/{id}', status_code=status.HTTP_202_ACCEPTED)
def get_student(id: int):
    for data in my_post:
        if data['id'] == id:
            return {"Student data": data}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No data found for ID {id}")

@app.get('/latest', status_code=status.HTTP_206_PARTIAL_CONTENT)
def get_latest():
    post = my_post[-1]
    return {"Latest student record": post}

@app.delete('/delete/{id}', status_code=status.HTTP_226_IM_USED)
def delete_student(id: int):
    index = helper_delete(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No student found with ID {id}")
    deleted_data = my_post.pop(index)
    return {"Deleted student record": deleted_data}

@app.put('/put/{id}', status_code=status.HTTP_200_OK)
def update_student(id: int, details: StudentDetails):
    index = helper_delete(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No student found with ID {id}")
    updated_student = details.dict()
    updated_student['id'] = id
    my_post[index] = updated_student
    return {"Updated student data": updated_student}
