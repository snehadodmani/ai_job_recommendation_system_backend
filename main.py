from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# ----------------------------
# App Initialization
# ----------------------------
app = FastAPI(
    title="AI Job Recommendation API",
    description="Skill-based Job Recommendation System (SDG 8)",
    version="1.0.0"
)

# ----------------------------
# CORS (IMPORTANT for frontend)
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all for demo/college project
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Job–Skill Knowledge Base
# ----------------------------
JOB_SKILL_MAP = {
    "Data Analyst": ["python", "sql", "statistics", "data analysis"],
    "AI Intern": ["python", "machine learning", "deep learning"],
    "Backend Developer": ["python", "api", "fastapi", "sql"],
    "Frontend Developer": ["html", "css", "javascript"],
    "Web Developer": ["html", "css", "javascript", "web development"],
    "ML Engineer": ["python", "machine learning", "data science"],
    "HR Executive": ["communication", "management"],
    "Customer Support Associate": ["communication"]
}

# ----------------------------
# Request Model
# ----------------------------
class UserInput(BaseModel):
    skills: List[str]
    education: Optional[str] = None
    experience: Optional[str] = None
    career_interest: Optional[str] = None

# ----------------------------
# Root Route (IMPORTANT)
# ----------------------------
@app.get("/")
def root():
    return {
        "message": "AI Job Recommendation API is running",
        "docs": "/docs"
    }

# ----------------------------
# Recommendation Endpoint
# ----------------------------
@app.post("/recommend")
def recommend_jobs(user: UserInput):
    user_skills = list(set([skill.lower().strip() for skill in user.skills]))

    recommendations = []

    for job, required_skills in JOB_SKILL_MAP.items():
        matched_skills = list(set(user_skills) & set(required_skills))
        if matched_skills:
            score = round(len(matched_skills) / len(required_skills), 2)
            recommendations.append({
                "job_role": job,
                "matched_skills": matched_skills,
                "confidence_score": score
            })

    # Sort by confidence score
    recommendations.sort(key=lambda x: x["confidence_score"], reverse=True)

    # Skill gap suggestion (top job only)
    skill_gap = []
    if recommendations:
        top_job = recommendations[0]["job_role"]
        skill_gap = list(set(JOB_SKILL_MAP[top_job]) - set(user_skills))

    return {
        "recommended_jobs": recommendations,
        "skill_gap_suggestions": skill_gap
    }

