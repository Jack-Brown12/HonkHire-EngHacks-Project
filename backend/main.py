from fastapi import FastAPI
from resume_matcher import calculate_resume_match

app = FastAPI()

@app.get("/")
def home():
    return {"message": "HireHonker backend is running"}

@app.post("/match")
def match_resume(data: dict):

    result = calculate_resume_match(
        data["resume_text"],
        data["core_skills"],
        data["skill_list"]
    )

    return result
