from pdf_ingestion import extract_text_from_pdf
from skill_extraction import extract_skills, detect_role
from resume_matcher import calculate_resume_match

def analyze_job_and_resume(job_pdf_path, resume_pdf_path):
    job_text = extract_text_from_pdf(job_pdf_path)
    resume_text = extract_text_from_pdf(resume_pdf_path)

    skills = extract_skills(job_text)
    role = detect_role(job_text)

    core_skills = [skill[0] for skill in skills]
    skill_list = [skill.lower() for skill in core_skills]

    result = calculate_resume_match(
        resume_text,
        core_skills,
        skill_list
    )

    return {
        "role": role,
        "skills": skills,
        "match_result": result
    }
