from fastapi import FastAPI, HTTPException
from skill_extraction.skill_extraction import extract_skills, detect_role
from pydantic import BaseModel, Field  
from typing import List

class JobPosting(BaseModel):
    job_description : str = Field(..., max_length=5000, description='WaterlooWorks Job PDF')

class ExtractedResponse(BaseModel):
    role: str
    skills: List[str]

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/extract_skills", response_model=ExtractedResponse)
def extract(data: JobPosting):
    text = data.job_description
    skills = extract_skills(text)
    role = detect_role(text)
    return {"role": role, "skills": skills}

