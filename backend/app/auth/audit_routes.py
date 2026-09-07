from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession
from app.core.security import Roles, require_roles
from app.db.session import get_db
from app.auth.audit import AuthAuditEvent

router = APIRouter()

@router.get("/")
def list_audit_events(user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    events = db.query(AuthAuditEvent).order_by(AuthAuditEvent.created_at.desc()).limit(100).all()
    return [{"id": e.id, "user_id": e.user_id, "event_type": e.event_type, "detail": e.detail, "created_at": str(e.created_at)} for e in events]