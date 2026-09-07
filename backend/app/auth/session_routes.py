from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession
from app.core.security import get_current_user
from app.db.session import get_db
from app.auth.sessions import UserSession, revoke_session, revoke_all_user_sessions

router = APIRouter()

@router.get("/")
def list_sessions(user: dict = Depends(get_current_user), db: DBSession = Depends(get_db)):
    sessions = db.query(UserSession).filter(UserSession.user_id == user["id"]).all()
    return [{"id": s.id, "token_family": s.token_family, "expires_at": str(s.expires_at), "revoked": s.revoked} for s in sessions]

@router.post("/{session_id}/revoke")
def revoke(session_id: str, user: dict = Depends(get_current_user), db: DBSession = Depends(get_db)):
    ok = revoke_session(db, session_id)
    if not ok:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Session not found")
    return {"revoked": True}

@router.post("/revoke-all")
def revoke_all(user: dict = Depends(get_current_user), db: DBSession = Depends(get_db)):
    count = revoke_all_user_sessions(db, user["id"])
    return {"revoked_count": count}