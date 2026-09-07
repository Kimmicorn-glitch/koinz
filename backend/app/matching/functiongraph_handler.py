from app.matching.service import skill_gap, weighted_score


def handler(event, _context):
    """FunctionGraph-compatible entrypoint for serverless scoring deployment."""
    required_skills = event.get("required_skills", [])
    candidate_skills = event.get("candidate_skills", [])
    experience_years = int(event.get("experience_years", 0))

    return {
        "score": weighted_score(required_skills, candidate_skills, experience_years),
        "missing_skills": skill_gap(required_skills, candidate_skills),
    }
