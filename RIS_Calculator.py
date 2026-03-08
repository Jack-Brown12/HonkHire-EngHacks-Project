def RIS_calculator(user_resume_skills, market_analysis):
    """
    :param user_resume_skills:
    :param market_analysis:
    :return a percentage score for the job's compatibility:
    """

    #Counters of the max possible and accumulative score
    score = 0
    max_possible_score = 0
    
    user_skills_set = {s.lower() for s in user_resume_skills}

    #Counts the skills classified as core
    for skill in market_analysis["core_skills"]:
        max_possible_score += 10
        if skill.lower() in user_skills_set:
            score += 10
        else:
            score -= 5

    #Counts the skills classified as optional or less common
    for skill in market_analysis["optional_skills"]:
        max_possible_score += 5
        if skill.lower() in user_skills_set:
            score += 5
        else: 
            score -= 2

    # Counts the skills classified as rare, which are worth more
    for skill in market_analysis["rare_skills"]:
        max_possible_score += 0
        if skill.lower() in user_skills_set:
            score += 5
        else: 
            score -= 0

    #Sets the baseline for the score to be a 0%
    if score <= 0: return 0

    #The output is meant to be a score percentage
    final_percentage = (score / max_possible_score) * 100

    #The maximum should be 100% capacity
    if final_percentage >= 100: return 100

    #Return the rounded final
    return round(final_percentage, 2)