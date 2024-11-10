import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DATABASE_URL = "dbname='student' user='postgres' password='lingavani' host='localhost' port='5432'"

app = FastAPI()

class Item(BaseModel):
    id: int = None
    name: str
    description: str

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id",
                (item.name, item.description)
            )
            item.id = cursor.fetchone()[0]
    return item

@app.get("/items/", response_model=list[Item])
def read_items():
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, description FROM items")
            rows = cursor.fetchall()
            return [Item(id=row[0], name=row[1], description=row[2]) for row in rows]

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, description FROM items WHERE id = %s", (item_id,))
            row = cursor.fetchone()
            if row is None:
                raise HTTPException(status_code=404, detail="Item not found")
            return Item(id=row[0], name=row[1], description=row[2])

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE items SET name = %s, description = %s WHERE id = %s",
                (item.name, item.description, item_id)
            )
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Item not found")
            item.id = item_id
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Item not found")
    return {"detail": "Item deleted"}
