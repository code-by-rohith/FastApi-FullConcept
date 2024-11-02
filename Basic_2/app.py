from fastapi import FastAPI, Response , status 
from fastapi import HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from typing import Optional

app =  FastAPI()


class Forum(BaseModel):
    name : str
    roll :int
    gender : Optional[str] = None

my_post = [{"name":"hari","roll":36,"id":1}]

@app.post('/payload' , status_code= status.HTTP_200_OK)
def create(payload : dict = Body(...)):
    print(payload)
    return {"message":payload}

@app.post('/post' , status_code= status.HTTP_201_CREATED)
def gett(req:Forum):
    pos =  req.dict()
    for data in my_post:
        if pos['roll'] ==  data['roll']:
            return {"message":"exist"}
    pos['id'] =  randrange(1,100000000)
    my_post.append(pos)
    print(my_post)
    return my_post


@app.get('/get/{id}' , status_code= status.HTTP_202_ACCEPTED)
def get_post(id:int):
    for data in my_post:
        if data['id'] == id:
            return {"Got !":data}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,
                        detail=f"No data found on {id}")

@app.get('/latest')
def get_latest():
    post = my_post[len(my_post)-1]
    return {"latest post" :post}