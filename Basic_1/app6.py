from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List

app = FastAPI()
MONGODB_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGODB_URL)
db = client.workflow
collection = db.market

class Product(BaseModel):
    name: str
    price: float

class ProductInDB(Product):
    id: str

def product_helper(product) -> ProductInDB:
    return ProductInDB(
        id=str(product["_id"]),
        name=product["name"],
        price=product["price"],
    )
@app.get('/get', response_model=List[ProductInDB])
async def get_all():
    products_cursor = collection.find()
    products = await products_cursor.to_list(length=None)
    return [product_helper(product) for product in products]

@app.get('/get/{product_id}', response_model=ProductInDB)
async def get_product(product_id: str):
    product = await collection.find_one({"_id": ObjectId(product_id)})
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_helper(product)
