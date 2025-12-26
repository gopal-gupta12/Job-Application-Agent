import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base
from dotenv import load_dotenv

load_dotenv('a.env')
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None :
    raise RuntimeError("DATABASE_URL is not set in enviornment variables")

engine = create_engine(DATABASE_URL) # object that knows how to talk to database(Neon) using connection URL , manages (opening, pooling, closing)
localSession = sessionmaker(autocommit = False, autoflush= False, bind = engine) # create sessions (short lived conversations with database) 
Base = declarative_base() # Base class that all ORM models inherit from. 

def get_db():
    db = localSession()
    try :
        yield db
    
    finally :
        db.close()