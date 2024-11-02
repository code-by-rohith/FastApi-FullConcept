from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Blog(BaseModel):
    name : str
    roll_no : int
    grnder : Optional[str]
    preset : bool



@app.post('/blog')
def blod_app(base:Blog):
    return {"message":f"blog is created {base.name}"} 