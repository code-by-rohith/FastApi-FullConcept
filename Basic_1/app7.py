from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Base(BaseModel):
    name :str
    roll_no:int
    marks:float

@app.get('/temp',response_model=Base)
def main(name,roll_no,marks):
    return {"name": name, "roll_no": roll_no, "marks": marks}

@app.post('/post')
def home(payload:dict):
    print(payload)
    return {"message":"Done"}
