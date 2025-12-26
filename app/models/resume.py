import uuid
from datetime import datetime
from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(
        UUID(as_uuid=True),  # gives globally unique IDs
        primary_key= True, 
        default= uuid.uuid4)
    
    base_resume = Column(Text, nullable = False)

    tailored_resume = Column(Text, nullable = False)
     
    # Links to the job this resume is tailored for 
    job_id = Column(
        UUID(as_uuid = True),
        ForeignKey("jobs.id"),
        nullable = False
    )

    job = relationship("Job", backref= "resumes") 

    

