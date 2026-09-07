from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession
from app.core.security import Roles, require_roles
from app.db.session import get_db
from app.risk.schemas import RiskEventCreate, RiskEventOut, RiskScoreOut, DetectionRuleOut
from app.risk.engine import record_risk_event, compute_risk_score, check_velocity, check_replay, initialize_default_rules
from app.risk.models import DetectionRule

router = APIRouter()

@router.post("/events", response_model=RiskEventOut)
def create_risk_event(payload: RiskEventCreate, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    event = record_risk_event(db, entity_id=payload.entity_id, event_type=payload.event_type, severity=payload.severity, reason_codes=payload.reason_codes, metadata=payload.metadata)
    return RiskEventOut(id=event.id, entity_id=event.entity_id, event_type=event.event_type, severity=event.severity, reason_codes=event.reason_codes, created_at=str(event.created_at))

@router.get("/scores/{entity_id}", response_model=RiskScoreOut)
def get_risk_score(entity_id: str, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    score = compute_risk_score(db, entity_id)
    return RiskScoreOut(id=score.id, entity_id=score.entity_id, score=score.score, version=score.version, reason_codes=score.reason_codes, model_version=score.model_version, computed_at=str(score.computed_at))

@router.get("/velocity/{entity_id}")
def velocity_check(entity_id: str, window_minutes: int = 60, max_count: int = 10, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    exceeded = check_velocity(db, entity_id, window_minutes, max_count)
    return {"entity_id": entity_id, "velocity_exceeded": exceeded}

@router.get("/replay/{entity_id}")
def replay_check(entity_id: str, external_id: str, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    detected = check_replay(db, entity_id, external_id)
    return {"entity_id": entity_id, "external_id": external_id, "replay_detected": detected}

@router.get("/rules", response_model=list[DetectionRuleOut])
def list_rules(user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    rules = db.query(DetectionRule).all()
    return [DetectionRuleOut(id=r.id, name=r.name, rule_type=r.rule_type, config=r.config, enabled=r.enabled) for r in rules]

@router.post("/initialize-rules")
def init_rules(user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    count = initialize_default_rules(db)
    return {"initialized": count}
