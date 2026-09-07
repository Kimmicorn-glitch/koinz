from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import Roles, get_current_user, require_roles
from app.db.session import get_db
from app.auth.mfa import generate_mfa_secret, verify_totp
from app.auth.mfa_schemas import MFASetupResponse, MFAVerifyRequest, MFAVerifyResponse
from app.core.crypto import encrypt_sensitive, decrypt_sensitive
from app.auth.mfa_models import MFAEnrollment
import uuid

router = APIRouter()

@router.post("/setup", response_model=MFASetupResponse)
def setup_mfa(user: dict = Depends(require_roles({Roles.WORKER, Roles.EMPLOYER, Roles.ADMIN})), db: Session = Depends(get_db)) -> MFASetupResponse:
    result = generate_mfa_secret()
    enrollment = MFAEnrollment(
        id=str(uuid.uuid4()),
        user_id=user["id"],
        secret_encrypted=encrypt_sensitive(result.secret),
        enabled=False,
    )
    db.add(enrollment)
    db.commit()
    return MFASetupResponse(secret=result.secret, otpauth_url=result.otpauth_url)

@router.post("/verify", response_model=MFAVerifyResponse)
def verify_mfa(payload: MFAVerifyRequest, user: dict = Depends(require_roles({Roles.WORKER, Roles.EMPLOYER, Roles.ADMIN})), db: Session = Depends(get_db)) -> MFAVerifyResponse:
    enrollment = db.query(MFAEnrollment).filter(
        MFAEnrollment.user_id == user["id"]
    ).order_by(MFAEnrollment.created_at.desc()).first()
    if not enrollment:
        return MFAVerifyResponse(verified=False)
    secret = decrypt_sensitive(enrollment.secret_encrypted)
    if verify_totp(secret, payload.code):
        enrollment.enabled = True
        db.commit()
        return MFAVerifyResponse(verified=True)
    return MFAVerifyResponse(verified=False)