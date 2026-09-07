from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from app.core.security import Roles, require_roles
from app.db.session import get_db
from app.learning.schemas import FeedbackCreate, FeedbackOut, ModelVersionCreate, ModelVersionOut, ChangeRequestCreate, ChangeRequestOut, AdvanceChangeRequest
from app.learning.service import create_feedback, create_model_version, deploy_model_version, create_change_request, advance_change_request, can_change_transition
from app.learning.models import ModelVersion, ChangeRequest

router = APIRouter()

@router.post("/feedback", response_model=FeedbackOut)
def add_feedback(payload: FeedbackCreate, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    fb = create_feedback(db, decision_id=payload.decision_id, feedback_type=payload.feedback_type, analyst_id=user["id"], notes=payload.notes)
    return FeedbackOut(id=fb.id, decision_id=fb.decision_id, feedback_type=fb.feedback_type, analyst_id=fb.analyst_id, notes=fb.notes, created_at=str(fb.created_at))

@router.get("/feedback", response_model=list[FeedbackOut])
def list_feedback(user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    from app.learning.models import Feedback
    fbs = db.query(Feedback).order_by(Feedback.created_at.desc()).limit(100).all()
    return [FeedbackOut(id=fb.id, decision_id=fb.decision_id, feedback_type=fb.feedback_type, analyst_id=fb.analyst_id, notes=fb.notes, created_at=str(fb.created_at)) for fb in fbs]

@router.post("/models", response_model=ModelVersionOut)
def create_model(payload: ModelVersionCreate, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    mv = create_model_version(db, model_name=payload.model_name, version=payload.version, config=payload.config)
    return ModelVersionOut(id=mv.id, model_name=mv.model_name, version=mv.version, config=mv.config, status=mv.status, deployed_by=mv.deployed_by, deployed_at=str(mv.deployed_at) if mv.deployed_at else None)

@router.post("/models/{model_id}/deploy", response_model=ModelVersionOut)
def deploy_model(model_id: str, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    mv = deploy_model_version(db, model_id, user["id"])
    if not mv:
        raise HTTPException(status_code=404, detail="Model version not found")
    return ModelVersionOut(id=mv.id, model_name=mv.model_name, version=mv.version, config=mv.config, status=mv.status, deployed_by=mv.deployed_by, deployed_at=str(mv.deployed_at) if mv.deployed_at else None)

@router.get("/models", response_model=list[ModelVersionOut])
def list_models(user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    mvs = db.query(ModelVersion).all()
    return [ModelVersionOut(id=mv.id, model_name=mv.model_name, version=mv.version, config=mv.config, status=mv.status, deployed_by=mv.deployed_by, deployed_at=str(mv.deployed_at) if mv.deployed_at else None) for mv in mvs]

@router.post("/changes", response_model=ChangeRequestOut)
def create_change(payload: ChangeRequestCreate, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    cr = create_change_request(db, title=payload.title, description=payload.description, change_type=payload.change_type, proposed_by=user["id"], metadata=payload.metadata)
    return ChangeRequestOut(id=cr.id, title=cr.title, description=cr.description, change_type=cr.change_type, status=cr.status, proposed_by=cr.proposed_by, reviewed_by=cr.reviewed_by, approved_by=cr.approved_by, created_at=str(cr.created_at), updated_at=str(cr.updated_at))

@router.post("/changes/{change_id}/advance", response_model=ChangeRequestOut)
def advance_change(change_id: str, payload: AdvanceChangeRequest, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    cr = advance_change_request(db, change_id, payload.target_status, user["id"])
    if not cr:
        raise HTTPException(status_code=400, detail="Invalid transition or change request not found")
    return ChangeRequestOut(id=cr.id, title=cr.title, description=cr.description, change_type=cr.change_type, status=cr.status, proposed_by=cr.proposed_by, reviewed_by=cr.reviewed_by, approved_by=cr.approved_by, created_at=str(cr.created_at), updated_at=str(cr.updated_at))

@router.get("/changes/{change_id}/transitions")
def get_transitions(change_id: str, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    cr = db.query(ChangeRequest).filter(ChangeRequest.id == change_id).first()
    if not cr:
        raise HTTPException(status_code=404, detail="Not found")
    from app.learning.service import CHANGE_TRANSITIONS
    return {"current": cr.status, "valid_transitions": CHANGE_TRANSITIONS.get(cr.status, [])}
