import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.schemas import LoginRequest, TokenResponse
from app.core.config import settings
from app.core.security import Roles, create_access_token, hash_password, verify_password
from app.db.session import SessionLocal


def authenticate_user(db: Session, payload: LoginRequest) -> User:
    user = db.query(User).filter(User.email == payload.email).first()
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return user


def login_user(db: Session, payload: LoginRequest) -> TokenResponse:
    user = authenticate_user(db, payload)
    token = create_access_token(subject=user.id, role=user.role)
    return TokenResponse(access_token=token, role=user.role)


def seed_default_users() -> None:
    db = SessionLocal()
    try:
        defaults = [
            {
                "email": settings.default_employer_email,
                "password": settings.default_employer_password,
                "full_name": "Default Employer",
                "role": Roles.EMPLOYER,
            },
            {
                "email": settings.default_worker_email,
                "password": settings.default_worker_password,
                "full_name": "Default Worker",
                "role": Roles.WORKER,
            },
        ]
        for item in defaults:
            exists = db.query(User).filter(User.email == item["email"]).first()
            if exists:
                continue
            db.add(
                User(
                    id=str(uuid.uuid4()),
                    email=item["email"],
                    full_name=item["full_name"],
                    hashed_password=hash_password(item["password"]),
                    role=item["role"],
                )
            )
        db.commit()
    finally:
        db.close()
