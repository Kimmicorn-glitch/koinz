import uuid

from sqlalchemy.orm import Session

from app.profile.models import WorkerProfile
from app.profile.schemas import ProfileCreate, ProfileResponse


def create_profile(db: Session, user_id: str, payload: ProfileCreate) -> ProfileResponse:
    profile = WorkerProfile(id=str(uuid.uuid4()), user_id=user_id, **payload.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)

    return ProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        full_name=profile.full_name,
        phone=profile.phone,
        township=profile.township,
        skills=profile.skills,
        resume_obs_key=profile.resume_obs_key,
    )
