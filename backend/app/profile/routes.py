from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user, require_roles, Roles
from app.db.session import get_db
from app.profile.schemas import ProfileCreate, ProfileResponse
from app.profile.service import create_profile

router = APIRouter()


@router.post("/", response_model=ProfileResponse)
def create(
    payload: ProfileCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles({Roles.WORKER, Roles.ADMIN})),
) -> ProfileResponse:
    return create_profile(db, user_id=user["id"], payload=payload)
