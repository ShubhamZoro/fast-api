from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()

class User(BaseModel):
    name: str
    age: int
    
all_todos=[
    {'todo_id': 1, 'todo_name': 'Sports','todo_description': 'Playing football'},
    {'todo_id': 2, 'todo_name': 'Study','todo_description': 'Studying math'}
]

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
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo['todo_id'] == todo_id:
            return {'result':todo}
    return {"message": "Todo not found"}

#path parameter

# @app.get("user/{user_id}")
# def road_user(user_id: int):
#     return {"user_id": user_id}

#query parameter
@app.get("/user/")
def road_user(user_id: int,name: str):
    return {"user_id": user_id, "name": name}

@app.get("/todos")
def get_todos(first_n:int=None):
    if first_n:
        return all_todos[:first_n]
    return all_todos

#path and query parameter
@app.get("/user/{user_id}/details")
def road_user_details(user_id: int,include_email: bool = False):
    if include_email:
        return {"user_id": user_id, "include email": "email included"}
    else:
        return {"user_id": user_id, "include email": "email not included"}
    
@app.get("/user/{user_id}", response_model=User)
async def get_user(user_id: int):
    return {"name": "John Doe", "age": 30}

@app.post('/todos')
def create_todo(todo: dict):
    new_todo_id= len(all_todos) + 1
    new_todo={
        'todo_id': new_todo_id,
        'todo_name': todo['todo_name'],
        'todo_description': todo['todo_description']
    }
    all_todos.append(todo)
    return new_todo

@app.put('/todos/{todo_id}')
def update_todo(todo_id: int, todo: dict):
    for t in all_todos:
        if t['todo_id'] == todo_id:
            t['todo_name'] = todo['todo_name']
            t['todo_description'] = todo['todo_description']
            return t
    return {"message": "Todo not found"}

@app.delete('/todos/{todo_id}')
def delete_todo(todo_id: int):
    for index, todo in enumerate(all_todos):
        if todo['todo_id'] == todo_id:
            deleted_todo = all_todos.pop(index)
            return deleted_todo
    return {"message": "Todo not found"}