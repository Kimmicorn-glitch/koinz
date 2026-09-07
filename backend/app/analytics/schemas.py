from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    total_profiles: int
    total_jobs: int
    match_success_rate: float
    monthly_placements: list[int]
