# app1.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    description: str = None
    price: float
    tags: List[str] = []


items = []

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    items.append(item)
    return item

@app.get("/items/", response_model=List[Item])
async def read_items():
    return items

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    return {"error": "Item not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
