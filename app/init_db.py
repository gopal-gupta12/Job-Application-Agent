from app.db import Base , engine
from app.models.job import Job
from app.models.application import Application
from app.models.resume import Resume

def init_database():
    """
    Create all tables defined on the Base metadata 
    in the connected database.
    """

Base.metadata.create_all(bind = engine) # Base.metadata holds a connection of all model and their table definitions.  create_all() sends create table.... statements to NeonDB for any missing value. This runs only once or occasionally to sync models to DB.

if __name__ == "__main__":

    init_database()