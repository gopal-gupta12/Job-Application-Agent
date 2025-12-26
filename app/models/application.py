import uuid
from datetime import datetime
from sqlalchemy import Column, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(
        UUID(as_uuid = True),
        primary_key= True, 
        default= uuid.uuid4
    ) 

    # which job was applied to 
    job_id = Column(
        UUID(as_uuid = True),
        ForeignKey("jobs.id"),
        nullable = False
    )

    # which tailored resume was used
    resume_id = Column(
        UUID(as_uuid= True),
        ForeignKey('resumes.id', ondelete = "CASCADE"),
        nullable = False
    )
    
    # timestamp when applicaton was sent 
    submitted_at = Column(DateTime, default = datetime.utcnow , nullable = False)

    job = relationship("Job")
    resume = relationship("Resume")