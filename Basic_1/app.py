from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()

class Item(BaseModel):
    name: str =...
    price: float
    id: Optional[int] = None
    published: bool = True
    review: Optional[int] = None


data = []

def finding(item_id: int):
    for value in data:
        if value['id'] == item_id:
            return value
    return None


@app.get('/get')
def read_root():
    return {"message": "Hello!"}

@app.get('/find/{id}')
def find_id(id: int):
    post = finding(id)
    if post is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"Detailed": post}

@app.get('/it')
def bydata():
    return {"data": data}

@app.post("/items")
async def create_item(item: Item):
    item_data = item.model_dump()
    item_data['id'] = randrange(0, 999999)
    data.append(item_data)
    return {"data": "Item received", "item": item_data}



