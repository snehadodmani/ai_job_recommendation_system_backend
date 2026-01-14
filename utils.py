def normalize_skills(skills):
    return list(set(skill.lower().strip() for skill in skills))
