import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Enum 
from sqlalchemy.dialects.postgresql import UUID
import enum

from app.db import Base

class JobStatus(str, enum.Enum) : # Subclassing from enum.Enum and str which ensures that Enum members behave like strings(useful for JSON and DB) , The DB Enum column stores these string values 
      scraped = "scraped"
      resume_prepared = "resume_prepared"
      applied = "applied"


class Job(Base):  # Declares the ORM model 'Job' , Inheriting from Base tells SQLAlchemy to treat this as a mapped table
      __tablename__ = "jobs" # Sets the actual table name in Postgres
      id = Column(
        UUID(as_uuid=True),  # gives globally unique IDs
        primary_key= True, 
        default= uuid.uuid4)
      
      title = Column(String , nullable= False)

      company = Column(String , nullable= False)

      description = Column(Text, nullable= False)

      url = Column(String, unique= True,  nullable = False) # 

      status = Column(Enum(JobStatus) # DB column constrained to the allowed enum values.
                      , nullable= False, default= JobStatus.scraped) # restricts status to valid values

      created_at = Column(DateTime, default= datetime.utcnow , nullable= False) #Records when job was created 

