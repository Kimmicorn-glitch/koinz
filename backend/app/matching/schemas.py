from pydantic import BaseModel, Field


class MatchItem(BaseModel):
    profile_id: str
    score: float = Field(ge=0.0, le=1.0)
    matched_skills: list[str]
    missing_skills: list[str]


class MatchResponse(BaseModel):
    job_id: str
    matches: list[MatchItem]
