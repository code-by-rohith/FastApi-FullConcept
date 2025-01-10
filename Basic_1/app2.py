from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import  asyncio

app = FastAPI()

class Item(BaseModel):
    name :str 
    roll : int
    total : float

@app.get('/')
async def main():
    return "Hello World"

@app.get('/get/{id}')
async def get(id : int):
    return {'id':id}

@app.get('/wet')
async  def wet( limit : int = 10 , publish : bool = False , sort : Optional[str] = None):
    if publish :
        return {"message":f" {limit} published from   db "}
    else :
        return {"message": f" nothing publisher since its false"}

@app.post('/data')
async def mains(items : Item):
    return items

@app.post('/post')
async def main(items:Item):
    return items



