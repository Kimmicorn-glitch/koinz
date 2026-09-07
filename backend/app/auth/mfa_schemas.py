from pydantic import BaseModel

class MFASetupResponse(BaseModel):
    secret: str
    otpauth_url: str

class MFAVerifyRequest(BaseModel):
    code: str

class MFAVerifyResponse(BaseModel):
    verified: bool

class SessionOut(BaseModel):
    id: str
    user_id: str
    token_family: str
    expires_at: str
    revoked: bool

class ConsentRequest(BaseModel):
    consent_type: str

class ConsentResponse(BaseModel):
    consent_type: str
    granted: bool

class AuthAuditEventOut(BaseModel):
    id: str
    user_id: str | None
    event_type: str
    detail: str
    created_at: str