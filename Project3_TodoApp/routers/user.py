from fastapi import APIRouter,Depends,Path,HTTPException, Query
from models import Todos,Users
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from routers.auth import get_current_user,hash_password,verify_password

router = APIRouter(
    prefix="/user",
    tags=['User']
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


class UserPassswordVerification(BaseModel):
    password: str
    new_password: str

# User endpoint to get the current logged in user info
@router.get("/my-info",status_code=status.HTTP_200_OK)
def get_current_user_info(user:USER_DEPENDENCY,db:DB_DEPENDENCY):
    """This function returns the details of the current logged in user"""
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Authentication failed!!")
    
    user_id = user.get('id')
    
    # Querying only required fields 
    user_info = db.query( 
        Users.username, Users.fullname, Users.email, Users.role, Users.is_active
    ).filter(Users.id == user_id).first()
    
    
    return user_info._asdict()


# Endpoint to change the current user password
@router.put("/change-password")
def change_password(user: USER_DEPENDENCY,db: DB_DEPENDENCY,user_verification: UserPassswordVerification):
    """This function changes the user password"""
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Authentication failed!!")
    
    user_id = user.get('id')
    # print(user_id)
    user_model = db.query(Users).filter(Users.id == user_id).first()
    
    current_password = user_verification.password
    new_password = user_verification.new_password
    
    # Verifying the current password with the user entered password
    if not verify_password(current_password,user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Authentication failed!!")
    
    user_model.hashed_password = hash_password(new_password)
    
     # Saving the existing todo with updates
    db.add(user_model)
    
    # Commiting to the db
    db.commit()
    
    return {"success":True,"message":"Password Changed succesfully!!"}
    