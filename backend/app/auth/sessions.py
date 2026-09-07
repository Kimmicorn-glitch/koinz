"""Session management with token families, expiry, and revocation."""
import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class UserSession(Base):
    __tablename__ = "user_sessions"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    token_family: Mapped[str] = mapped_column(String(64), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

def create_session(db, user_id: str, expire_minutes: int = 120) -> UserSession:
    from app.db.session import SessionLocal
    session = UserSession(
        id=str(uuid.uuid4()),
        user_id=user_id,
        token_family=str(uuid.uuid4()),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=expire_minutes),
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def revoke_session(db, session_id: str) -> bool:
    session = db.query(UserSession).filter(UserSession.id == session_id).first()
    if not session:
        return False
    session.revoked = True
    db.commit()
    return True

def revoke_all_user_sessions(db, user_id: str) -> int:
    count = db.query(UserSession).filter(UserSession.user_id == user_id, UserSession.revoked == False).update({"revoked": True})
    db.commit()
    return count

def is_session_valid(session: UserSession) -> bool:
    return not session.revoked and session.expires_at > datetime.now(timezone.utc)