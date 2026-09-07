from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.auth.service import seed_default_users
from app.core.config import settings
from app.core.ratelimit import InMemoryRateLimiter
from app.db.base import Base
from app.db.session import engine
from app.models import MFAEnrollment, UserSession, ConsentRecord, AuthAuditEvent, IngestedAccount, IngestedTransaction, IngestedBeneficiary, IngestedMandate, BankAccount, CashoutVoucher, EmployerFunding, Job, LedgerEntry, PaymentIdempotency, User, Wallet, WorkerPayout, WorkerProfile, AuditEvent, ChangeRequest, EncryptedField, ExecutionRequest, ExecutionResult, Feedback, KeyRotationLog, ModelVersion, ReconciliationRecord


@asynccontextmanager
async def lifespan(_app: FastAPI):
    if settings.environment.lower() not in {"production", "prod"}:
        Base.metadata.create_all(bind=engine)
    seed_default_users()
    yield


app = FastAPI(title=settings.project_name, version=settings.app_version, lifespan=lifespan)
settings.validate_production_security()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)

rate_limiter = InMemoryRateLimiter()


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    if settings.security_headers_enabled:
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        response.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
        response.headers.setdefault("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; img-src 'self' data:; object-src 'none'; frame-ancestors 'none'; base-uri 'self'",
        )
    return response


@app.middleware("http")
async def rate_limit(request: Request, call_next):
    path = request.url.path
    client_ip = request.client.host if request.client else "unknown"
    if path == "/auth/login":
        key = f"login:{client_ip}"
        if not rate_limiter.allow(key, settings.rate_limit_login_per_minute, 60):
            return JSONResponse(status_code=429, content={"detail": "Too many login attempts. Try again later."})
    if path.startswith("/payments"):
        key = f"payments:{client_ip}"
        if not rate_limiter.allow(key, settings.rate_limit_payments_per_minute, 60):
            return JSONResponse(status_code=429, content={"detail": "Too many payment requests. Slow down."})
    return await call_next(request)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.project_name, "environment": settings.environment}