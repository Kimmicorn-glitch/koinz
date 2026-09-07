"""Authorization audit log — login attempts, role changes, privilege escalation."""
import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class AuthAuditEvent(Base):
    __tablename__ = "auth_audit_events"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    detail: Mapped[str] = mapped_column(String(500), default="")
    ip_address: Mapped[str] = mapped_column(String(64), default="unknown")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

def log_auth_event(db, *, user_id: str | None, event_type: str, detail: str = "", ip_address: str = "unknown") -> AuthAuditEvent:
    event = AuthAuditEvent(
        id=str(uuid.uuid4()),
        user_id=user_id,
        event_type=event_type,
        detail=detail,
        ip_address=ip_address,
    )
    db.add(event)
    db.commit()
    return event