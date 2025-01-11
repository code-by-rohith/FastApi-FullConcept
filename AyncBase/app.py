from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List

app = FastAPI()
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.library
collection = db.books

class Book(BaseModel):
    title: str
    author: str
    year: int

class BookInDB(Book):
    id: str

def book_helper(book) -> BookInDB:
    return BookInDB(
        id=str(book["_id"]),
        title=book["title"],
        author=book["author"],
        year=book["year"]
    )

@app.post("/create", response_model=BookInDB)
async def create_book(book: Book):
    book_dict = book.dict()
    result = await collection.insert_one(book_dict)
    created_book = await collection.find_one({"_id": result.inserted_id})
    return book_helper(created_book)

@app.get("/read/{book_id}", response_model=BookInDB)
async def read_book(book_id: str):
    book = await collection.find_one({"_id": ObjectId(book_id)})
    if book:
        return book_helper(book)
    raise HTTPException(status_code=404, detail="Book not found")

@app.put("/update/{book_id}", response_model=BookInDB)
async def update_book(book_id: str, book: Book):
    updated_book = await collection.find_one_and_update(
        {"_id": ObjectId(book_id)},
        {"$set": book.dict()},
        return_document=True
    )
    if updated_book:
        return book_helper(updated_book)
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/delete/{book_id}")
async def delete_book(book_id: str):
    result = await collection.delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count == 1:
        return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books", response_model=List[BookInDB])
async def get_books():
    books = []
    async for book in collection.find():
        books.append(book_helper(book))
    return books
