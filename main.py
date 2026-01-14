from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from utils import normalize_skills
from recommender import recommend_jobs

app = FastAPI(title="AI Job Recommendation Agent")

# ✅ CORS FIX (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputPayload(BaseModel):
    skills: list
    education: str | None = None
    experience: str | None = None
    career_interest: str | None = None

@app.post("/recommend")
def get_recommendations(data: InputPayload):
    if not data.skills:
        raise HTTPException(status_code=400, detail="Skills are required")

    skills = normalize_skills(data.skills)
    jobs = recommend_jobs(skills)

    if not jobs:
        return {
            "message": "No matching jobs found. Try adding more skills.",
            "skill_gap_suggestions": ["python", "sql", "communication"]
        }

    return {
        "recommended_jobs": jobs,
        "note": "Recommendations are guidance, not guarantees."
    }
