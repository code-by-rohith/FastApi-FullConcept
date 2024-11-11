import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
import time
import random

app = FastAPI()

class Item(BaseModel):
    title: str
    content: str
    published: bool = True


def get_db_connection():
    while True:
        try:
            conn = psycopg2.connect(host='localhost', database='student', user='postgres',
                                     password='lingavani', cursor_factory=RealDictCursor)
            return conn
        except Exception as e:
            print(f'Connection failed! Error: {e}')
            time.sleep(4)


def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS post (
        id INT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        content TEXT NOT NULL,
        published BOOLEAN NOT NULL DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

create_table()

@app.get('/get')
def getting():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM post")
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"data": posts}

@app.post('/post')
def posting(post: Item):
    random_id = random.randint(1000, 9999) 
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """INSERT INTO post (id, title, content, published) 
           VALUES (%s, %s, %s, %s) RETURNING *""",
        (random_id, post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"data": new_post}
