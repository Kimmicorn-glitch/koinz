from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from app.core.security import Roles, require_roles
from app.db.session import get_db
from app.decision.schemas import DecisionCreate, DecisionOut, AIRecommendationCreate, AIRecommendationOut, ReviewRequest
from app.decision.engine import create_decision, create_ai_recommendation, review_decision

router = APIRouter()

@router.post("/", response_model=DecisionOut)
def make_decision(payload: DecisionCreate, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    d = create_decision(db, entity_id=payload.entity_id, decision_type=payload.decision_type, outcome=payload.outcome, reason=payload.reason, policy_ids=payload.policy_ids, risk_score_id=payload.risk_score_id, created_by=user["id"])
    return DecisionOut(id=d.id, entity_id=d.entity_id, decision_type=d.decision_type, outcome=d.outcome, reason=d.reason, policy_ids=d.policy_ids, reviewer_id=d.reviewer_id, created_by=d.created_by, created_at=str(d.created_at))

@router.get("/", response_model=list[DecisionOut])
def list_decisions(user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    from app.decision.models import Decision
    decisions = db.query(Decision).order_by(Decision.created_at.desc()).limit(100).all()
    return [DecisionOut(id=d.id, entity_id=d.entity_id, decision_type=d.decision_type, outcome=d.outcome, reason=d.reason, policy_ids=d.policy_ids, reviewer_id=d.reviewer_id, created_by=d.created_by, created_at=str(d.created_at)) for d in decisions]

@router.post("/recommendations", response_model=AIRecommendationOut)
def add_recommendation(payload: AIRecommendationCreate, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    r = create_ai_recommendation(db, decision_id=payload.decision_id, recommendation=payload.recommendation, confidence=payload.confidence, reasons=payload.reasons, explanation=payload.explanation)
    return AIRecommendationOut(id=r.id, decision_id=r.decision_id, recommendation=r.recommendation, confidence=r.confidence, reasons=r.reasons, model_version=r.model_version, explanation=r.explanation)

@router.post("/{decision_id}/review", response_model=DecisionOut)
def review(decision_id: str, payload: ReviewRequest, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    d = review_decision(db, decision_id, user["id"], payload.outcome)
    if not d:
        raise HTTPException(status_code=404, detail="Decision not found")
    return DecisionOut(id=d.id, entity_id=d.entity_id, decision_type=d.decision_type, outcome=d.outcome, reason=d.reason, policy_ids=d.policy_ids, reviewer_id=d.reviewer_id, created_by=d.created_by, created_at=str(d.created_at))
