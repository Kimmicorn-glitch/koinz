"""Risk detection engine with velocity checks, replay detection, and scoring."""
import uuid
from datetime import datetime, timezone, timedelta
from collections import defaultdict

from sqlalchemy.orm import Session

from app.risk.models import RiskEvent, RiskScore, DetectionRule

DEFAULT_RULES = [
    {"name": "velocity_check", "rule_type": "velocity", "config": {"max_transactions": 10, "window_minutes": 60}},
    {"name": "replay_detection", "rule_type": "replay", "config": {"duplicate_window_minutes": 5}},
    {"name": "amount_threshold", "rule_type": "amount", "config": {"max_amount_cents": 10000000}},
    {"name": "suspicious_beneficiary", "rule_type": "beneficiary", "config": {"flag_new_beneficiary": True}},
]

def _score_from_events(events: list[RiskEvent]) -> float:
    severity_map = {"low": 0.1, "medium": 0.3, "high": 0.6, "critical": 1.0}
    if not events:
        return 0.0
    total = sum(severity_map.get(e.severity, 0.1) for e in events)
    return min(total / len(events), 1.0)

def compute_risk_score(db: Session, entity_id: str) -> RiskScore:
    events = db.query(RiskEvent).filter(RiskEvent.entity_id == entity_id).order_by(RiskEvent.created_at.desc()).limit(50).all()
    score = _score_from_events(events)
    reason_codes = []
    for e in events:
        reason_codes.extend(e.reason_codes if isinstance(e.reason_codes, list) else [])
    latest_version = db.query(RiskScore).filter(RiskScore.entity_id == entity_id).order_by(RiskScore.version.desc()).first()
    version = (latest_version.version + 1) if latest_version else 1
    risk_score = RiskScore(
        id=str(uuid.uuid4()),
        entity_id=entity_id,
        score=score,
        version=version,
        reason_codes=reason_codes[:20],
        model_version="v1.0",
    )
    db.add(risk_score)
    db.commit()
    db.refresh(risk_score)
    return risk_score

def record_risk_event(db: Session, *, entity_id: str, event_type: str, severity: str, reason_codes: list[str] | None = None, metadata: dict | None = None) -> RiskEvent:
    event = RiskEvent(
        id=str(uuid.uuid4()),
        entity_id=entity_id,
        event_type=event_type,
        severity=severity,
        reason_codes=reason_codes or [],
        event_metadata=metadata or {},
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def check_velocity(db: Session, entity_id: str, window_minutes: int = 60, max_count: int = 10) -> bool:
    """Returns True if velocity limit is exceeded."""
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=window_minutes)
    count = db.query(RiskEvent).filter(
        RiskEvent.entity_id == entity_id,
        RiskEvent.event_type == "transaction",
        RiskEvent.created_at >= cutoff,
    ).count()
    return count >= max_count

def check_replay(db: Session, entity_id: str, external_id: str, window_minutes: int = 5) -> bool:
    """Returns True if a duplicate transaction is detected."""
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=window_minutes)
    count = db.query(RiskEvent).filter(
        RiskEvent.entity_id == entity_id,
        RiskEvent.event_type == "transaction",
        RiskEvent.event_metadata.contains({"external_id": external_id}),
        RiskEvent.created_at >= cutoff,
    ).count()
    return count > 0

def initialize_default_rules(db: Session) -> int:
    count = 0
    for rule in DEFAULT_RULES:
        existing = db.query(DetectionRule).filter(DetectionRule.name == rule["name"]).first()
        if not existing:
            db.add(DetectionRule(id=str(uuid.uuid4()), **rule))
            count += 1
    if count:
        db.commit()
    return count
