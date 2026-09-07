"""Decision engine with AI recommendations, confidence, and hard boundaries."""
import uuid
from sqlalchemy.orm import Session
from app.decision.models import Decision, AIRecommendation

def create_decision(db: Session, *, entity_id: str, decision_type: str, outcome: str, reason: str = "", policy_ids: list[str] | None = None, risk_score_id: str | None = None, created_by: str = "system") -> Decision:
    decision = Decision(
        id=str(uuid.uuid4()),
        entity_id=entity_id,
        decision_type=decision_type,
        outcome=outcome,
        reason=reason,
        policy_ids=policy_ids or [],
        risk_score_id=risk_score_id,
        created_by=created_by,
    )
    db.add(decision)
    db.commit()
    db.refresh(decision)
    return decision

def create_ai_recommendation(db: Session, *, decision_id: str, recommendation: str, confidence: float, reasons: list[str] | None = None, model_version: str = "v1.0", explanation: str = "") -> AIRecommendation:
    confidence = max(0.0, min(1.0, confidence))
    rec = AIRecommendation(
        id=str(uuid.uuid4()),
        decision_id=decision_id,
        recommendation=recommendation,
        confidence=confidence,
        reasons=reasons or [],
        model_version=model_version,
        explanation=explanation,
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec

def review_decision(db: Session, decision_id: str, reviewer_id: str, outcome: str) -> Decision | None:
    from datetime import datetime, timezone
    decision = db.query(Decision).filter(Decision.id == decision_id).first()
    if not decision:
        return None
    decision.outcome = outcome
    decision.reviewer_id = reviewer_id
    decision.reviewed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(decision)
    return decision
