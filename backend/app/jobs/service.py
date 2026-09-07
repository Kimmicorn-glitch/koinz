import uuid

from sqlalchemy.orm import Session

from app.jobs.models import Job
from app.jobs.schemas import JobCreate, JobResponse


def create_job(db: Session, employer_id: str, payload: JobCreate) -> JobResponse:
    job = Job(id=str(uuid.uuid4()), employer_id=employer_id, **payload.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)

    return JobResponse(
        id=job.id,
        employer_id=job.employer_id,
        title=job.title,
        description=job.description,
        location=job.location,
        required_skills=job.required_skills,
    )
