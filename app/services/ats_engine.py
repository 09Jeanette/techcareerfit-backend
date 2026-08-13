from app.services.cv_parser import SKILL_KEYWORDS


def extract_job_skills(description: str) -> list[str]:
    lower_text = description.lower()

    return [
        skill for skill in SKILL_KEYWORDS
        if skill in lower_text
    ]


def score_cv_against_job(cv_skills: list[str], job_skills: list[str]) -> dict:
    cv_skills_set = set(cv_skills)
    job_skills_set = set(job_skills)

    if not job_skills_set:
        return {
            "score": 0,
            "missing_skills": [],
            "recommendations": [
                "No recognizable skills found in the job description — "
                "consider expanding the skill keyword list."
            ]
        }

    matched = cv_skills_set & job_skills_set
    missing = sorted(job_skills_set - cv_skills_set)

    score = round((len(matched) / len(job_skills_set)) * 100)

    recommendations = [
        f"Consider adding or highlighting experience with: {skill}"
        for skill in missing
    ]

    if not missing:
        recommendations = ["Your CV covers all detected skills for this job description."]

    return {
        "score": score,
        "missing_skills": missing,
        "recommendations": recommendations
    }