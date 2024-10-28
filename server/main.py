from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

books = []

class Book(BaseModel):
    title: str
    author: str
    year: int


@app.get("/books")
async def get_books():
    return books


@app.post("/books")
async def add_book(book: Book):
    books.append(book.dict()) 
    return {"message": "Book added successfully!"}

