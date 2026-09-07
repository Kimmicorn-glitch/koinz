from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession
from app.core.security import get_current_user
from app.db.session import get_db
from app.auth.consent import grant_consent, withdraw_consent, has_consent
from app.auth.mfa_schemas import ConsentRequest, ConsentResponse

router = APIRouter()

@router.post("/", response_model=ConsentResponse)
def grant(payload: ConsentRequest, user: dict = Depends(get_current_user), db: DBSession = Depends(get_db)):
    grant_consent(db, user["id"], payload.consent_type)
    return ConsentResponse(consent_type=payload.consent_type, granted=True)

@router.post("/withdraw", response_model=ConsentResponse)
def withdraw(payload: ConsentRequest, user: dict = Depends(get_current_user), db: DBSession = Depends(get_db)):
    ok = withdraw_consent(db, user["id"], payload.consent_type)
    return ConsentResponse(consent_type=payload.consent_type, granted=False)

@router.get("/check")
def check(consent_type: str, user: dict = Depends(get_current_user), db: DBSession = Depends(get_db)):
    return {"consent_type": consent_type, "granted": has_consent(db, user["id"], consent_type)}