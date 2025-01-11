from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import threading
import time

app = FastAPI()

# In-memory storage for demonstration purposes
fake_db = {}


class Item(BaseModel):
    name: str
    description: str = None


# Helper function to simulate a blocking task
def blocking_task(task_name: str):
    print(f"Starting {task_name}...")
    time.sleep(2)  # Simulate blocking task, e.g., database I/O
    print(f"{task_name} completed!")


# CREATE operation
@app.post("/items/")
async def create_item(item: Item):
    # Simulating a blocking task in a separate thread
    thread = threading.Thread(target=blocking_task, args=("Creating item",))
    thread.start()

    # Storing item in the fake database (simulated)
    fake_db[item.name] = item
    return {"message": "Item created successfully", "item": item}


# READ operation
@app.get("/items/{item_name}")
async def read_item(item_name: str):
    # Simulating a blocking task in a separate thread
    thread = threading.Thread(target=blocking_task, args=("Reading item",))
    thread.start()

    item = fake_db.get(item_name)
    if item:
        return {"item": item}
    raise HTTPException(status_code=404, detail="Item not found")


# UPDATE operation
@app.put("/items/{item_name}")
async def update_item(item_name: str, item: Item):
    # Simulating a blocking task in a separate thread
    thread = threading.Thread(target=blocking_task, args=("Updating item",))
    thread.start()

    if item_name in fake_db:
        fake_db[item_name] = item
        return {"message": "Item updated successfully", "item": item}
    raise HTTPException(status_code=404, detail="Item not found")


# DELETE operation
@app.delete("/items/{item_name}")
async def delete_item(item_name: str):
    # Simulating a blocking task in a separate thread
    thread = threading.Thread(target=blocking_task, args=("Deleting item",))
    thread.start()

    if item_name in fake_db:
        del fake_db[item_name]
        return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

# Run FastAPI application
