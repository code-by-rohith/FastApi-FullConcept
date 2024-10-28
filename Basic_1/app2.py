from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name :str 
    roll : int
    total : float

@app.get('/')
def main():
    return "Hello World"

@app.get('/get/{id}')
def get(id : int):
    return {'id':id}

@app.get('/wet')
def wet( limit : int = 10 , publish : bool = False , sort : Optional[str] = None):
    if publish :
        return {"message":f" {limit} published from   db "}
    else :
        return {"message": f" nothing publisher since its false"}

@app.post('/data')
def mains(items : Item):
    return items

@app.post('/post')
def main(items:Item):
    return items



