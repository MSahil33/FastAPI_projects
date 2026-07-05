from fastapi import FastAPI,Depends
from models import Todos,Base
from database import engine
from typing import Annotated
from sqlalchemy.orm import Session
from routers import auth,todos,admin,user


app = FastAPI()


# Creating database if not created from Base
Base.metadata.create_all(bind=engine)


# Creating a home endpoints
@app.get("/")
def home():
    return {"message":"Hello Welcome to Todos Backend ! Health Status : Ok👍"}

# Setting the router for other endpoints
app.include_router(admin.router) # For admin access and operations
app.include_router(auth.router) # For user authentication
app.include_router(user.router) # For user access and operations
app.include_router(todos.router) # For Todos operations