from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel
from models import Users
from sqlalchemy.orm import Session
from typing import Annotated
from database import SessionLocal
from starlette import status
from sqlalchemy.exc import IntegrityError #Raising error for sql constraint failure
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from datetime import timedelta,datetime,timezone
from jose import jwt,JWTError

# Using for password hashing
from passlib.context import CryptContext

# Using Bcrypt for password hashing
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Creating a oauth bearer for user authorization
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/access-token')

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
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


# Secret key and algorithm for authorization with JWT
SECRET_KEY = "305ebb33545c32f5a5e9869de1abc98d36df92b8fe3037d78acdfa74cab22406"
ALGORITHM = "HS256"

class CreateUserRequest(BaseModel):
    username: str
    full_name: str
    email: str
    password: str
    role: str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
# Helper function to hash the user password
def hash_password(user_password: str)-> str:
    return bcrypt_context.hash(user_password)

# Helper function to verify the user password against the hashed password
def verify_password(user_password:str, hashed_password:str)-> bool:
    return bcrypt_context.verify(user_password,hashed_password)

# Helper function to authenticate user from db
def authenticate_user(username:str,password: str,db):
    """Helper function to authenticate user"""
    
    user = db.query(Users).filter(Users.username == username).first()
    
    if not user:
        return False
    
    # Verifying the user plain password with hashed password 
    if not verify_password(password,user.hashed_password):
        return False

    return user
     
# Function to create a acces token
def create_acces_token(username:str,user_id:int,user_role: str,expire_delta:timedelta):
    payload = {"sub":username,'id':user_id,'user_role':user_role}
    expires = datetime.now(timezone.utc) + expire_delta
    payload['exp'] = expires
    
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

# Function to get the current logged_in user
async def get_current_user(token: Annotated[str,Depends(oauth2_bearer)]):
    try:
        
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('user_role')
        
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate user!!")
        
        return {'username':username,"id":user_id,'user_role':user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate user!!")

# Endpoint to get the acces token for user login 
@router.post("/access-token",response_model=Token)
def login_for_acces_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],db: DB_DEPENDENCY):
    
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate user!!")
    
    access_token = create_acces_token(user.username,user.id,user.role,timedelta(hours=1))
    
    return {"message":"Acces token created succesfully!","access_token":access_token,"token_type":"bearer"}

# Endpoint to create a new user
@router.post("/create-user",status_code=status.HTTP_201_CREATED)
def create_user(db:DB_DEPENDENCY, create_user_request: CreateUserRequest):
    
    """This function creates a new user with hashed password and store it in the database."""
    new_user_model = Users(
        username= create_user_request.username,
        fullname= create_user_request.full_name,
        email= create_user_request.email,
        hashed_password= hash_password(create_user_request.password),
        role= create_user_request.role,
        is_active= True
    )
        
    try:
        # Stroing the new user detail in the database
        db.add(new_user_model)
        db.commit()
        
        # Refreshing the new user from db
        db.refresh(new_user_model)
        return {"user_id":new_user_model.id,"message":"User added Successfully"}
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig)

        if "users.username" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists."
            )
        elif "users.email" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unique constraint violated. Please check username/email."
            )
            