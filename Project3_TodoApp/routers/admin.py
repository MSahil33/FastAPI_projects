from fastapi import APIRouter,Depends,Path,HTTPException, Query
from models import Todos,Users
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from routers.auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=['Admin']
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


# Read all the todos
@router.get("/all-todos",status_code=status.HTTP_200_OK)
def get_all_todos(user: USER_DEPENDENCY,db:DB_DEPENDENCY):
    """This functions returns all the todos to the admin"""
    
    
    if user is None or user.get('user_role')!='admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized access!!")
    
    print("User : ",user)
    todos = db.query(Todos).all()
    
    return {"todos":todos,"total_count":len(todos)}


# Endpoint to get all the users
@router.get("/all-users",status_code=status.HTTP_200_OK)
def get_all_users(user:USER_DEPENDENCY,db: DB_DEPENDENCY):
    """This function gets all the users from the db"""
    
    if user is None or user.get('user_role')!='admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized access!!")
    
    all_users = db.query(Users).all()
    
    users = all_users
    message = "Users fetched successfully!!"
    user_count = len(users)
    if all_users is None:
        message = "No users found"
        users = []
        user_count = 0
    return {"message":message,"users":users,"total_users":user_count}
    
    
