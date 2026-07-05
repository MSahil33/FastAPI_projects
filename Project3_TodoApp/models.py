from database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey

# Sample Data -- Sample data for Todos table
# INSERT INTO "Todos" (title, description, priority, "isCompleted") VALUES
# ('Buy groceries', 'Buy milk, eggs, and bread from the supermarket', 2, FALSE),
# ('Finish project report', 'Complete and submit the quarterly project report', 1, TRUE),
# ('Workout', 'Attend gym session for 1 hour', 3, FALSE),
# ('Pay bills', 'Pay electricity and internet bills before due date', 2, TRUE),
# ('Call Mom', 'Check in with mom over the phone', 3, FALSE),
# ('Plan weekend trip', 'Decide destination and book tickets for the trip', 4, FALSE),
# ('Read book', 'Read 30 pages of a new novel', 5, FALSE),
# ('Clean room', 'Organize desk and clean the bedroom', 4, TRUE),
# ('Attend meeting', 'Team sync-up meeting at 10 AM', 1, TRUE),
# ('Learn SQL', 'Practice subqueries and joins for 1 hour', 3, FALSE);

#  A Model for our todos table
class Todos(Base):
    
    __tablename__ = "todos"
    
    # Defining Columns for the table
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    isCompleted = Column(Boolean,default=False)
    owner_id = Column(Integer,ForeignKey('users.id'))
    
    
class Users(Base):
    
    __tablename__="users"
    
    # Defining the columns for Users
    id = Column(Integer,primary_key=True,index=True)
    fullname = Column(String)
    username = Column(String,unique=True)
    email = Column(String,unique=True)
    hashed_password = Column(String)
    role = Column(String)
    is_active = Column(Boolean,default=True)

    
    
    