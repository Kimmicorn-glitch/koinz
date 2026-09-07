from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.analytics.schemas import AnalyticsOverview
from app.analytics.service import get_overview
from app.core.security import Roles, require_roles
from app.db.session import get_db

router = APIRouter()


@router.get("/overview", response_model=AnalyticsOverview)
def overview(
    db: Session = Depends(get_db),
    _user: dict = Depends(require_roles({Roles.EMPLOYER, Roles.ADMIN})),
) -> AnalyticsOverview:
    return get_overview(db)
