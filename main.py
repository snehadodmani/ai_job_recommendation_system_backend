from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="AI Job Recommendation API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

JOB_SKILL_MAP = {
    "Data Analyst": ["python", "sql", "statistics"],
    "AI Intern": ["python", "machine learning"],
    "Backend Developer": ["python", "fastapi", "sql"],
    "Frontend Developer": ["html", "css", "javascript"],
    "Web Developer": ["html", "css", "javascript"],
    "ML Engineer": ["python", "machine learning"],
    "HR Executive": ["communication"],
}

class UserInput(BaseModel):
    skills: List[str]
    education: Optional[str] = None
    experience: Optional[str] = None
    career_interest: Optional[str] = None

@app.get("/")
def root():
    return {
        "message": "AI Job Recommendation API is running",
        "docs": "/docs"
    }

@app.post("/recommend")
def recommend(user: UserInput):
    user_skills = [s.lower().strip() for s in user.skills]
    results = []

    for job, skills in JOB_SKILL_MAP.items():
        matched = list(set(user_skills) & set(skills))
        if matched:
            score = round(len(matched) / len(skills), 2)
            results.append({
                "job_role": job,
                "matched_skills": matched,
                "confidence_score": score
            })

    results.sort(key=lambda x: x["confidence_score"], reverse=True)

    skill_gap = []
    if results:
        top_job = results[0]["job_role"]
        skill_gap = list(set(JOB_SKILL_MAP[top_job]) - set(user_skills))

    return {
        "recommended_jobs": results,
        "skill_gap_suggestions": skill_gap
    }
