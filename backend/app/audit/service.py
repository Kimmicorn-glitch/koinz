"""Audit service with hash-chain integrity and reporting."""
import hashlib
import json
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.audit.models import AuditEvent

def _compute_hash(correlation_id: str, event_type: str, entity_id: str, payload: dict, previous_hash: str, sequence_number: int) -> str:
    data = json.dumps({
        "correlation_id": correlation_id,
        "event_type": event_type,
        "entity_id": entity_id,
        "payload": payload,
        "previous_hash": previous_hash,
        "sequence_number": sequence_number,
    }, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()

def record_audit_event(db: Session, *, correlation_id: str, event_type: str, entity_type: str, entity_id: str, actor_id: str = "system", payload: dict | None = None) -> AuditEvent:
    last_event = db.query(AuditEvent).order_by(AuditEvent.sequence_number.desc()).first()
    seq = (last_event.sequence_number + 1) if last_event else 1
    prev_hash = last_event.event_hash if last_event else "0" * 64
    event_hash = _compute_hash(correlation_id, event_type, entity_id, payload or {}, prev_hash, seq)
    event = AuditEvent(
        id=str(uuid.uuid4()),
        correlation_id=correlation_id,
        event_type=event_type,
        entity_type=entity_type,
        entity_id=entity_id,
        actor_id=actor_id,
        payload=payload or {},
        previous_hash=prev_hash,
        event_hash=event_hash,
        sequence_number=seq,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def verify_hash_chain(db: Session, start: int = 0, end: int | None = None) -> dict:
    query = db.query(AuditEvent).filter(AuditEvent.sequence_number >= start)
    if end is not None:
        query = query.filter(AuditEvent.sequence_number <= end)
    events = query.order_by(AuditEvent.sequence_number).all()
    if not events:
        return {"valid": True, "events_checked": 0}
    prev_hash = "0" * 64
    checked = 0
    for event in events:
        if event.previous_hash != prev_hash:
            return {"valid": False, "break_at": event.sequence_number, "events_checked": checked}
        expected_hash = _compute_hash(event.correlation_id, event.event_type, event.entity_id, event.payload, event.previous_hash, event.sequence_number)
        if event.event_hash != expected_hash:
            return {"valid": False, "tampered_at": event.sequence_number, "events_checked": checked}
        prev_hash = event.event_hash
        checked += 1
    return {"valid": True, "events_checked": checked}

def get_events_by_correlation(db: Session, correlation_id: str) -> list[AuditEvent]:
    return db.query(AuditEvent).filter(AuditEvent.correlation_id == correlation_id).order_by(AuditEvent.sequence_number).all()

def generate_transaction_report(db: Session) -> dict:
    total = db.query(AuditEvent).filter(AuditEvent.event_type == "transaction").count()
    by_type = {}
    events = db.query(AuditEvent).filter(AuditEvent.event_type == "transaction").all()
    for e in events:
        t = e.payload.get("type", "unknown")
        by_type[t] = by_type.get(t, 0) + 1
    return {"total_transactions": total, "by_type": by_type, "generated_at": datetime.now(timezone.utc).isoformat()}
