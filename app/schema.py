from datetime import datetime 
from typing import Optional
from uuid import UUID
from pydantic import BaseModel # Provides Runtime type validation , and Automatic type conversion, and clear error messages, and easy json serialization.

class JobCreate(BaseModel):  # client send this when creating a job
    title : str
    company : str
    description : str
    url : str


class JobRead(BaseModel): # Server returns this when snding a job(no id, status, or created_at. those are set by server).
    id : UUID
    title : str
    company : str
    description : str
    url : str
    status : str
    created_at : datetime

    class Config:
        from_attributes = True # Lets Pydantic read from SQLAlchemy models.
