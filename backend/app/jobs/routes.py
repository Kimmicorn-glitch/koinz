from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import Roles, require_roles
from app.db.session import get_db
from app.jobs.schemas import JobCreate, JobResponse
from app.jobs.service import create_job

router = APIRouter()


@router.post("/", response_model=JobResponse)
def create(
    payload: JobCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles({Roles.EMPLOYER, Roles.ADMIN})),
) -> JobResponse:
    return create_job(db, employer_id=user["id"], payload=payload)
