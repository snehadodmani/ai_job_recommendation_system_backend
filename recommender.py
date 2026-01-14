from job_skill_mapping import JOB_SKILL_MAP

def recommend_jobs(user_skills):
    recommendations = []

    for job, required_skills in JOB_SKILL_MAP.items():
        matched = list(set(user_skills) & set(required_skills))
        if matched:
            score = round(len(matched) / len(required_skills), 2)
            recommendations.append({
                "job_role": job,
                "matched_skills": matched,
                "confidence_score": score
            })

    recommendations.sort(key=lambda x: x["confidence_score"], reverse=True)
    return recommendations
