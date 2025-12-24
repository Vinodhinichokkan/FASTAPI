from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()

@app.get("/")
def read_root():  
    return {"message": "Welcome to the FastAPI application!"}

li = []

@app.get("/items")
def read():
    return {"items": li}

class Item(BaseModel):
    name: str
    age:int


@app.post("/items/create")
def create(item: Item):
    paylod = {
        "id": len(li),
        "name": item.name,
        "age": item.age
    }
    li.append(paylod)
    return {"message": "Item added successfully", "item": li}

@app.put("/items/update/{item_id}")
def update(item_id: int, item: Item):
    for i in li:
        if i["id"] == item_id:
            i["name"] = item.name
            i["age"] = item.age
            return {"message": "Item updated successfully", "item": i}
    # return{"message": "Item not found"}
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/items/delete/{item_id}")
def delete(item_id: int):
    for i in li:
        if i["id"] == item_id:
            li.remove(i)
            return {"message": "Item deleted successfully", "item": li}
    # return{"message": "Item not found"}
    raise HTTPException(status_code=404, detail="Item not found")