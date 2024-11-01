from fastapi import FastAPI  , Depends
from . import schemas
from . import models
from .database import engine , SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db =  SessionLocal()
    try :
        yield db
    finally:
        db.close()


@app.post('/blog')
def create(blog:schemas.Blog , db : Session =  Depends(get_db)):
    new_blog = models.Blog(tittle = blog.tittle , body = blog.body )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog