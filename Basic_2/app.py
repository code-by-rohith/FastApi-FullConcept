from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import motor.motor_asyncio
from pydantic import BaseModel

MONGO_DETAILS = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.users_db
users_collection = database.get_collection("users")


app = FastAPI()
templates = Jinja2Templates(directory="templates")
class User(BaseModel):
    username: str
    email: str
    password: str
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/register", response_class=HTMLResponse)
async def register(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    existing_user = await users_collection.find_one({"username": username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    await users_collection.insert_one({"username": username, "email": email, "password": password})

    return templates.TemplateResponse("index.html", {"request": request, "message": "User registered!"})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = await users_collection.find_one({"username": username})
    if not user or user.get("password") != password:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    return templates.TemplateResponse("index.html", {"request": request, "message": "Login successful!"})


