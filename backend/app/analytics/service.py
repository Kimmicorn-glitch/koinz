from sqlalchemy import func
from sqlalchemy.orm import Session

from app.analytics.schemas import AnalyticsOverview
from app.jobs.models import Job
from app.profile.models import WorkerProfile


def get_overview(db: Session) -> AnalyticsOverview:
    total_profiles = db.query(func.count(WorkerProfile.id)).scalar() or 0
    total_jobs = db.query(func.count(Job.id)).scalar() or 0

    # TODO: Wire this metric to actual placements table when onboarding pipeline is implemented.
    match_success_rate = 0.78 if total_jobs else 0.0

    return AnalyticsOverview(
        total_profiles=total_profiles,
        total_jobs=total_jobs,
        match_success_rate=match_success_rate,
        monthly_placements=[8, 12, 14, 18, 21, 19],
    )
