def extract_resume_skills(resume_text, skill_list):
    resume_text = resume_text.lower()
    found_skills = []

    for skill in skill_list:
        if skill.lower() in resume_text and skill.lower() not in found_skills:
            found_skills.append(skill.lower())

    return found_skills


def calculate_resume_match(resume_text, core_skills, skill_list):
    resume_skills = extract_resume_skills(resume_text, skill_list)

    core_skills_lower = [skill.lower() for skill in core_skills]
    matched_skills = [skill for skill in core_skills_lower if skill in resume_skills]
    missing_skills = [skill for skill in core_skills_lower if skill not in resume_skills]

    if len(core_skills_lower) == 0:
        match_score = 0
    else:
        match_score = round((len(matched_skills) / len(core_skills_lower)) * 100)

    if match_score >= 75:
        status = "Competitive"
    elif match_score >= 40:
        status = "Borderline"
    else:
        status = "Unlikely"

    return {
        "resume_skills": resume_skills,
        "matched_core_skills": matched_skills,
        "missing_core_skills": missing_skills,
        "resume_match": match_score,
        "status": status
    }
