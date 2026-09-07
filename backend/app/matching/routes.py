from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.matching.schemas import MatchResponse
from app.matching.service import get_matches

router = APIRouter()


@router.get("/{job_id}", response_model=MatchResponse)
def matches(job_id: str, _user: dict = Depends(get_current_user)) -> MatchResponse:
    return get_matches(job_id)
