from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession
from app.core.security import Roles, require_roles
from app.db.session import get_db
from app.audit.schemas import AuditEventCreate, AuditEventOut, HashChainVerification, TransactionReport
from app.audit.service import record_audit_event, verify_hash_chain, get_events_by_correlation, generate_transaction_report

router = APIRouter()

@router.post("/events", response_model=AuditEventOut)
def create_event(payload: AuditEventCreate, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    e = record_audit_event(db, correlation_id=payload.correlation_id, event_type=payload.event_type, entity_type=payload.entity_type, entity_id=payload.entity_id, actor_id=user["id"], payload=payload.payload)
    return AuditEventOut(id=e.id, correlation_id=e.correlation_id, event_type=e.event_type, entity_type=e.entity_type, entity_id=e.entity_id, actor_id=e.actor_id, sequence_number=e.sequence_number, event_hash=e.event_hash, created_at=str(e.created_at))

@router.get("/events/{correlation_id}", response_model=list[AuditEventOut])
def by_correlation(correlation_id: str, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    events = get_events_by_correlation(db, correlation_id)
    return [AuditEventOut(id=e.id, correlation_id=e.correlation_id, event_type=e.event_type, entity_type=e.entity_type, entity_id=e.entity_id, actor_id=e.actor_id, sequence_number=e.sequence_number, event_hash=e.event_hash, created_at=str(e.created_at)) for e in events]

@router.get("/verify-chain", response_model=HashChainVerification)
def verify(start: int = 0, end: int | None = None, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    result = verify_hash_chain(db, start, end)
    return HashChainVerification(**result)

@router.get("/reports/transactions", response_model=TransactionReport)
def transaction_report(user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    return TransactionReport(**generate_transaction_report(db))
