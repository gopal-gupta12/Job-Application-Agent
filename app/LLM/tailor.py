import os
from groq import Groq
from app.models.job import Job

client = Groq(
    api_key = os.environ.get("GROQ_API_KEY"),
)

SYSTEM_PROMPT = """
You are a resume optimaztion assistant.

You recieve :
1) The candidate's resume base text.
2) A specific job description.

Task:
-Rewrite the resume to empasize skills, projects, and experience that match the job.
-Remove or downplay irrelavent content.
-Keep everything factual , do not invent experience.
-Use clear sections and bullet points when helpful.
-Return only the final tailored resume text. 
""".strip()

def t