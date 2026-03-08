def RIS_calculator(user_resume_skills, market_analysis):
    score = 0
    max_possible_score = 0
    
    user_skills_set = {s.lower() for s in user_resume_skills}

    for skill in market_analysis["core_skills"]:
        max_possible_score += 10
        if skill.lower() in user_skills_set:
            score += 10
        else:
            score -= 20

    for skill in market_analysis["optional_skills"]:
        max_possible_score += 5
        if skill.lower() in user_skills_set:
            score += 5
        else: 
            score -= 2

    
    for skill in market_analysis["rare_skills"]:
        max_possible_score += 0
        if skill.lower() in user_skills_set:
            score += 25
        else: 
            score -= 0

    if score <= 0: return 0

    final_percentage = (score / max_possible_score) * 100

    if final_percentage >= 100: return 100
    
    return round(final_percentage, 2)