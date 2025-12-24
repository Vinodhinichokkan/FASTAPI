from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")["Demodb"]["test"]

app = FastAPI()

def data():
    return list(client.find({}, {"_id": 0}))


@app.get("/")
def read_root():  
    return {"message": "Welcome to the FastAPI application!"}


@app.get("/items")
def read():
    user_data = data()
    return {"items": user_data}

class Item(BaseModel):
    name: str
    age:int


@app.post("/items/create")
def create(item: Item):
    paylod = {
        "id": len(data())+1,
        "name": item.name,
        "age": item.age
    }
    try:
        client.insert_one(paylod)                   
        return {"message": "Item added successfully", "item": data()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 


@app.put("/items/update/{item_id}")
def update(item_id: int, item: Item):
    try:
        if client.find_one({"id": item_id}):
            client.update_one(
                {"id": item_id},
                {"$set": {
                    "name": item.name,
                    "age": item.age
                }}
            )
            return {"message": "Item updated successfully", "item": data()}
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/items/delete/{item_id}")
def delete(item_id: int):
    try:
        if client.find_one({"id": item_id}):
            client.delete_one({"id": item_id})
            return {"message": "Item deleted successfully", "item": data()}
        # return{"message": "Item not found"}
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))