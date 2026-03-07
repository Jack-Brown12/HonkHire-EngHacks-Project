def RIS_calculator(resume_skills, matched_skills, missing_skills, match_score, skill_category_lists):
    score = 0

    common_skills = skill_category_lists["core_skills"]
    uncommon_skills = skill_category_lists["optional_skills"]
    rare_skills = skill_category_lists["optional_skills"]

    for skill in matched_skills:
        if skill in common_skills:
            score += 1
        elif skill in uncommon_skills:
            score += 2
        elif skill in rare_skills:
            score += 3

    for skill in missing_skills:
        if skill in common_skills:
            score -= 3
        elif skill in uncommon_skills:
            score -= 2
        elif skill in rare_skills:
            score -= 1

    if score > 0:
        eval = 1
    elif score < 0:
        eval = -1
    else:
        eval = 0

    return eval