"""User consent records with withdrawal support."""
import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class ConsentRecord(Base):
    __tablename__ = "consent_records"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    consent_type: Mapped[str] = mapped_column(String(64), nullable=False)
    granted: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    withdrawn_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

def grant_consent(db, user_id: str, consent_type: str) -> ConsentRecord:
    record = ConsentRecord(id=str(uuid.uuid4()), user_id=user_id, consent_type=consent_type, granted=True)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def withdraw_consent(db, user_id: str, consent_type: str) -> bool:
    record = db.query(ConsentRecord).filter(
        ConsentRecord.user_id == user_id,
        ConsentRecord.consent_type == consent_type,
        ConsentRecord.granted == True,
    ).first()
    if not record:
        return False
    record.granted = False
    record.withdrawn_at = datetime.now(timezone.utc)
    db.commit()
    return True

def has_consent(db, user_id: str, consent_type: str) -> bool:
    record = db.query(ConsentRecord).filter(
        ConsentRecord.user_id == user_id,
        ConsentRecord.consent_type == consent_type,
    ).order_by(ConsentRecord.created_at.desc()).first()
    return record is not None and record.granted