from fastapi import APIRouter,Depends,Path,HTTPException, Query
from models import Todos
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from routers.auth import get_current_user

router = APIRouter(
    prefix="/todo",
    tags=["Todos"]
)

# Creating a generator to get the db whenever we do a db operation
def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
           
# Creating a database dependency (i,e dependency injection) such that whenever a endpoint uses db operation is there db dependency is used such that it should be yielded when needed and gets close after yielding
DB_DEPENDENCY = Annotated[Session,Depends(getDB)]

# Creating a user dependency such that if a user is currently logged in or not to check before any todo operations
USER_DEPENDENCY = Annotated[dict,Depends(get_current_user)]

# TodoRequest Pydantic Model for a Todo with validations
class TodoRequest(BaseModel):
    
    title : str = Field(min_length=3)
    description : str = Field(min_length=3,max_length=100)
    priority : int = Field(gt=0,lt=6)
    isCompleted : bool
    
# Endpoint to get all the todos from the db of the current logged in user
@router.get("/all",status_code=status.HTTP_200_OK)
def get_all_todos(user: USER_DEPENDENCY,db:DB_DEPENDENCY):
    """This Returns all the todos from the db of the current logged in user"""
    
    if user is None:
        raise HTTPException(status_code=401,detail="Unauthorized user!!")
        
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

# Endpoint to get a todo by ID of the current logged in user
@router.get("/{todo_id}",status_code=status.HTTP_200_OK)
def get_todo_by_id(user: USER_DEPENDENCY,db:DB_DEPENDENCY,todo_id: int = Path(gt=0)):
    """This function returns the first occurence of the todo found by their id of the current logged in user"""
    
    if user is None:
        raise HTTPException(status_code=401,detail="Unauthorized user!!")
        
    todo_res = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    
    if todo_res is not None:
        return todo_res
    
    raise HTTPException(status_code=404,detail=f"Todo not found for the id : {todo_id}")

@router.post("/add",status_code=status.HTTP_201_CREATED)
def add_todo(user:USER_DEPENDENCY,db:DB_DEPENDENCY,todo: TodoRequest):
    """This function adds a new todo in the database"""
    
    try:
        if user is None:
            raise HTTPException(status_code=401,detail="Unauthorized user!!")
        
        # Creating a todo model for db
        todo_model = Todos(**todo.model_dump(),owner_id=user.get('id'))
        
        # Adding to db
        db.add(todo_model)
        
        # Commiting to db
        db.commit()
        
        return {"message":"New Todo added successfully!!"}
    except:
        raise HTTPException(status_code=500,detail={"message":"Todo creation failed!!"})
    
@router.put("/update")
def update_todo(user:USER_DEPENDENCY,db:DB_DEPENDENCY, todo_req:TodoRequest, todo_id:int = Query(gt=0)):
    """This function updates the todo based on the todo id"""

    if user is None:
        raise HTTPException(status_code=401,detail="Unauthorized user!!")
        
    # Fetching the existing todo by id from db
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404,detail=f"No todo found for the id : {todo_id}")
    
    # Updating the existing todo model
    todo_model.title = todo_req.title
    todo_model.description = todo_req.description
    todo_model.priority = todo_req.priority
    todo_model.isCompleted = todo_req.isCompleted
    
    # Saving the existing todo with updates
    db.add(todo_model)
    
    # Commiting to the db
    db.commit()
    
    return {"message":"Todo updated successfully"}

@router.delete("/delete")
def delete_todo(user: USER_DEPENDENCY,db:DB_DEPENDENCY,todo_id:int = Query(gt=0)):
    """This function deletes a todo from the db"""
    if user is None:
        raise HTTPException(status_code=401,detail="Unauthorized user!!")
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404,detail=f"No todo found for the id:{todo_id} to delete")
    
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()
    
    db.commit()
    
    return {"message": f"Todo deleted successfully for id : {todo_id}"}
       