from typing import List # List is a type hint to say "this endpoint returns a list of items". It Helps FastAPI generate docs and validate responses. 
from fastapi import FastAPI , Depends, HTTPException # Depends is a FastAPI's dependency injection system: lets us declare that a function parameter(eg db) should be provided by another function(get_db).
from sqlalchemy.orm import Session 
from uuid import UUID
from app.models.job import Job
from app.db import get_db

from app.schema import JobRead, JobCreate

from app.scrapers.fake_jobs import scrape_fake_jobs

from app.LLM.tailor import tailor_resume

from app.models.resume import Resume
app = FastAPI() #Instantiates the application object. app is used by Uvicorn.

# Health check endpoint: quickly checks if the server is running 
@app.get("/health") 
def health_check(): 
    return {"status": "ok"}

# job endpoint :
@app.get("/jobs", response_model= List[JobRead]) # tells FastApi to convert ORM object to JobRead , And validate and document the reponse model.
# db is typed as a SQLAlchemy Session. Before calling list_jobs, FastAPI will : *call get_db() to obtain a session. *inject it into db. *after the request finishes, run the finally part to close the session.
def list_jobs(db: Session = Depends(get_db)): 
    jobs = db.query(Job).all() #Uses the session to query the jobs table via the Job model. db.query(Job) builds a SELECT for jobs. .all() executes it and returns a list of Job instances.
    return jobs


# Allowing Backend to create and save new jobs in the database through an HTTP API :
@app.post("/jobs", response_model = JobCreate) 
def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    job = Job(    # Creates an ORM object
        title = payload.title,
        company = payload.company,
        description = payload.description,
        url = payload.url,
    )
    
    db.add(job) # mark object for insertion
    db.commit() # executes the INSERT on Neon
    db.refresh(job) # reloads from DB (now it has id, created_at and status).
    
    return job # FastAPI converts to JobRead using from_attributes


@app.post("/scrape/fake")
def scrape_and_store_fake_jobs(db: Session = Depends(get_db)):
    scraped_jobs = scrape_fake_jobs() # Calls pure python scraper; returns a list of dictionaries.

    new_count = 0

    for j in scraped_jobs:
        existing = db.query(Job).filter(Job.url == j["url"]).first() # Prevents duplicates when you call the endpoint multiple times.
        
        if existing :
            continue

        job = Job( # Creates ORM object and marks it for insertion. 
            title = j["title"],
            company = j["company"],
            decription = j["description"],
            url = j["url"],
        )

        db.add(job)
        new_count += 1  

    db.commit()  

    return {"inserted" : new_count, "total_scraped" : len(scraped_jobs)}


@app.post("/jobs/{job_id}/tailor")
def tailor_job_resume(job_id : UUID,db: Session = Depends(get_db)):
    """
    Generate and store a tailored resume for the given job_id.
    """

    # Find job in the database 
    job = db.query(Job).filter(Job.id == job_id).first()
    if job is None :
        raise HTTPException(status_code=404, detail="Job not found")

    base_resume_text = """"
    Gopal Gupta
    Machine Learning Engineer

    Skills :
    - Python, FastAPI
    - Machine Learning :
    Scikit-learn, basic deep learning
    - Web Srapping: requests, BeautifulSoup 
    
    Experience :
    - Built small ML projects and APIs for learning.
    """.strip()
   
     
    # Calling LLM to get the tailored resume text :
    tailored_text = tailor_resume(
        base_resume=base_resume_text,
        job_description=job.description
    )
    
    # Creates and stored a Resume row linked to this job :
    resume_row = Resume(
     base_resume = base_resume_text,
     tailor_resume = tailored_text,
     job_id = job.id,
    )

    db.add(resume_row)
    db.commit()
    db.refresh(resume_row)

    return {
        "job_id" : str(job.id),
        "resume_id" : str(resume_row.id),
        "tailored_resume" : resume_row.tailored_resume
    }