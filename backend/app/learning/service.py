"""Controlled learning service with PROPOSE -> REVIEW -> TEST -> APPROVE -> VERSION -> DEPLOY -> MONITOR workflow."""
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.learning.models import Feedback, ModelVersion, ChangeRequest

CHANGE_TRANSITIONS = {
    "proposed": ["review"],
    "review": ["test", "rejected"],
    "test": ["approve"],
    "approve": ["version", "rejected"],
    "version": ["deploy"],
    "deploy": ["monitor"],
    "monitor": [],
    "rejected": [],
}

def can_change_transition(current: str, target: str) -> bool:
    return target in CHANGE_TRANSITIONS.get(current, [])

def create_feedback(db: Session, *, decision_id: str, feedback_type: str, analyst_id: str, notes: str = "") -> Feedback:
    fb = Feedback(
        id=str(uuid.uuid4()),
        decision_id=decision_id,
        feedback_type=feedback_type,
        analyst_id=analyst_id,
        notes=notes,
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb

def create_model_version(db: Session, *, model_name: str, version: str, config: dict | None = None) -> ModelVersion:
    mv = ModelVersion(
        id=str(uuid.uuid4()),
        model_name=model_name,
        version=version,
        config=config or {},
    )
    db.add(mv)
    db.commit()
    db.refresh(mv)
    return mv

def deploy_model_version(db: Session, model_version_id: str, deployed_by: str) -> ModelVersion | None:
    mv = db.query(ModelVersion).filter(ModelVersion.id == model_version_id).first()
    if not mv:
        return None
    mv.status = "deployed"
    mv.deployed_by = deployed_by
    mv.deployed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(mv)
    return mv

def create_change_request(db: Session, *, title: str, description: str, change_type: str, proposed_by: str, metadata: dict | None = None) -> ChangeRequest:
    cr = ChangeRequest(
        id=str(uuid.uuid4()),
        title=title,
        description=description,
        change_type=change_type,
        proposed_by=proposed_by,
        metadata_value=metadata or {},
    )
    db.add(cr)
    db.commit()
    db.refresh(cr)
    return cr

def advance_change_request(db: Session, change_id: str, target_status: str, actor_id: str) -> ChangeRequest | None:
    cr = db.query(ChangeRequest).filter(ChangeRequest.id == change_id).first()
    if not cr:
        return None
    if not can_change_transition(cr.status, target_status):
        return None
    cr.status = target_status
    if target_status == "review":
        cr.reviewed_by = actor_id
    elif target_status == "approve":
        cr.approved_by = actor_id
    cr.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(cr)
    return cr
