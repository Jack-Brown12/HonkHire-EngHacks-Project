def RIS_calculator(user_resume_skills, market_analysis):
    score = 0
    max_possible_score = 0
    
    user_skills_set = {s.lower() for s in user_resume_skills}

    for skill in market_analysis["core_skills"]:
        max_possible_score += 1
        if skill.lower() in user_skills_set:
            score += 1
        else:
            score -= 1

    for skill in market_analysis["optional_skills"]:
        max_possible_score += 2
        if skill.lower() in user_skills_set:
            score += 2
        else: 
            score -= 2

    
    for skill in market_analysis["rare_skills"]:
        max_possible_score += 3
        if skill.lower() in user_skills_set:
            score += 3  
        else: 
            score -= 3

           

    final_percentage = 
    
    
    return round(final_percentage, 2)