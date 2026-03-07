from skill_extraction import extract_skills
from pdf_ingestion import extract_text_from_pdf 

def calculate_resume_match(resume_text, job_text):
   
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)
    
    matched_skills = [skill for skill in resume_skills if skill in job_skills]
    
    missing_skills = [skill for skill in job_skills if skill not in resume_skills]

    if not job_skills: 
        match_score = 0
    else:
        match_score = round((len(matched_skills) / len(job_skills)) * 100)

    
    return {
        "resume_skills": resume_skills,
        "matched_core_skills": matched_skills,
        "missing_core_skills": missing_skills,
        "resume_match": match_score,
    }
