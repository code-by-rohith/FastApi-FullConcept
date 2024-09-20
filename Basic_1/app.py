from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Define a Pydantic model
class DetailResponse(BaseModel):
    name: str

class UserResponse(BaseModel):
    users: List[str]

@app.get('/detail', response_model=DetailResponse)
def main():
    return DetailResponse(name="rohtih")

@app.get("/pro/{data_id}")
def home(data_id: int):
    return {"value": data_id}

@app.get("/users", response_model=UserResponse)
async def read_users():
    return UserResponse(users=["Rick", "Morty"])

@app.get("/users2", response_model=UserResponse)
async def read_users2():
    return UserResponse(users=["Bean", "Elfo"])




