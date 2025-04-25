from fastapi import FastAPI
app=FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcoeme to the FastAPI application!"}

@app.post("/items/")
def create_item(name: str, price: float):
    return {"name": name, "price": price}

@app.put("/items/{item_id}")
def update_item(item_id: int, name: str, price: float):
    return {"item_id": item_id, "name": name, "price": price}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": f"Item with id {item_id} has been deleted."}

#path parameter

@app.get("user/{user_id}")
def road_user(user_id: int):
    return {"user_id": user_id}

#query parameter
@app.get("/user/")
def road_user(user_id: int,name: str):
    return {"user_id": user_id, "name": name}

#path and query parameter
@app.get("/user/{user_id}/details")
def road_user_details(user_id: int,include_email: bool = False):
    if include_email:
        return {"user_id": user_id, "include email": "email included"}
    else:
        return {"user_id": user_id, "include email": "email not included"}
    