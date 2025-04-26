from typing import List, Optional
from enum import IntEnum
from fastapi import FastAPI,HTTPException  
from pydantic import BaseModel,Field
app=FastAPI()

class User(BaseModel):
    name: str
    age: int
    
    
class Priority(IntEnum):
    low = 1
    medium = 2
    high = 3

class TodoBase(BaseModel):
    todo_name: str=Field(..., min_length=3, max_length=512,description="Name of the todo")
    todo_description: str=Field(...,description="Description of the todo")
    priority: Priority = Field(default=Priority.low, description="Priority of the todo")

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    todo_id: int=Field(..., description="Unique identifier of the todo")


class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=3, max_length=512, description="Name of the todo")
    todo_description: Optional[str] = Field(None, description="Description of the todo")
    priority: Optional[Priority] = Field(None, description="Priority of the todo")

all_todos=[
    Todo(todo_id=1,todo_name='Sports',todo_description='Playing football',priority=Priority.low),
    Todo(todo_id=2,todo_name='Study',todo_description='Studying math',priority=Priority.medium),
    Todo(todo_id=3,todo_name='Work',todo_description='Working on project',priority=Priority.high),
    Todo(todo_id=4,todo_name='Exercise',todo_description='Doing exercise',priority=Priority.low),
    Todo(todo_id=5,todo_name='Reading',todo_description='Reading books',priority=Priority.medium)
]

# @app.get("/")
# def read_root():
#     return {"message": "Welcoeme to the FastAPI application!"}

# @app.post("/items/")
# def create_item(name: str, price: float):
#     return {"name": name, "price": price}

# @app.put("/items/{item_id}")
# def update_item(item_id: int, name: str, price: float):
#     return {"item_id": item_id, "name": name, "price": price}

# @app.delete("/items/{item_id}")
# def delete_item(item_id: int):
#     return {"message": f"Item with id {item_id} has been deleted."}

#path parameter
@app.get("/todos/{todo_id}",response_model=Todo)
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

#path parameter

# @app.get("user/{user_id}")
# def road_user(user_id: int):
#     return {"user_id": user_id}

#query parameter
# @app.get("/user/")
# def road_user(user_id: int,name: str):
#     return {"user_id": user_id, "name": name}

@app.get("/todos",response_model=List[Todo])
def get_todos(first_n:int=None):
    if first_n:
        return all_todos[:first_n]
    return all_todos

#path and query parameter
# @app.get("/user/{user_id}/details")
# def road_user_details(user_id: int,include_email: bool = False):
#     if include_email:
#         return {"user_id": user_id, "include email": "email included"}
#     else:
#         return {"user_id": user_id, "include email": "email not included"}
    
# @app.get("/user/{user_id}", response_model=User)
# async def get_user(user_id: int):
#     return {"name": "John Doe", "age": 30}

@app.post('/todos', response_model=Todo)
def create_todo(todo: TodoCreate):
    new_todo_id= len(all_todos) + 1
    new_todo=Todo(
        todo_id=new_todo_id,
        todo_name=todo.todo_name,
        todo_description=todo.todo_description,
        priority=todo.priority
    )
    
    all_todos.append(new_todo)
    return new_todo

@app.put('/todos/{todo_id}',response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate):
    for t in all_todos:
        if t.todo_id == todo_id:
            if updated_todo.todo_name is not None:
                t.todo_name = updated_todo.todo_name
            if updated_todo.todo_description is not None:
                t.todo_description = updated_todo.todo_description
            if updated_todo.priority is not None:
                t.priority = updated_todo.priority
            
            return t
    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete('/todos/{todo_id}',response_model=Todo)
def delete_todo(todo_id: int):
    for index, todo in enumerate(all_todos):
        if todo.todo_id == todo_id:
            deleted_todo = all_todos.pop(index)
            return deleted_todo
    raise HTTPException(status_code=404, detail="Todo not found")