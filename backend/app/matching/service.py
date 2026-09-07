from app.matching.schemas import MatchItem, MatchResponse


def skill_gap(required_skills: list[str], candidate_skills: list[str]) -> list[str]:
    required = {s.strip().lower() for s in required_skills if s.strip()}
    candidate = {s.strip().lower() for s in candidate_skills if s.strip()}
    return sorted(required - candidate)


def weighted_score(required_skills: list[str], candidate_skills: list[str], experience_years: int = 0) -> float:
    required = {s.strip().lower() for s in required_skills if s.strip()}
    candidate = {s.strip().lower() for s in candidate_skills if s.strip()}

    if not required:
        return 0.0

    overlap = required & candidate
    skill_ratio = len(overlap) / len(required)
    experience_boost = min(experience_years / 10, 1.0)

    score = (skill_ratio * 0.85) + (experience_boost * 0.15)
    return round(min(score, 1.0), 4)


def get_matches(job_id: str) -> MatchResponse:
    # TODO: Replace static profile inventory with DB-backed candidate retrieval.
    required = ["electrical", "safety", "maintenance"]
    candidates = [
        {"id": "wrk-001", "skills": ["electrical", "maintenance"], "experience_years": 5},
        {
            "id": "wrk-002",
            "skills": ["electrical", "safety", "maintenance", "inspection"],
            "experience_years": 2,
        },
    ]

    ranked: list[MatchItem] = []
    for candidate in candidates:
        candidate_skills = candidate["skills"]
        missing = skill_gap(required, candidate_skills)
        matched = sorted({s.lower() for s in required if s.lower() in {c.lower() for c in candidate_skills}})
        ranked.append(
            MatchItem(
                profile_id=candidate["id"],
                score=weighted_score(required, candidate_skills, candidate["experience_years"]),
                matched_skills=matched,
                missing_skills=missing,
            )
        )

    ranked.sort(key=lambda item: item.score, reverse=True)
    return MatchResponse(job_id=job_id, matches=ranked)
