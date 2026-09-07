from fastapi import APIRouter
from app.analytics.routes import router as analytics_router
from app.auth.routes import router as auth_router
from app.auth.mfa_routes import router as mfa_router
from app.auth.session_routes import router as session_router
from app.auth.consent_routes import router as consent_router
from app.auth.audit_routes import router as audit_router
from app.jobs.routes import router as jobs_router
from app.matching.routes import router as matching_router
from app.payments.routes import router as payments_router
from app.profile.routes import router as profile_router
from app.ingestion.routes import router as ingestion_router
from app.enrichment.routes import router as enrichment_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(mfa_router, prefix="/auth/mfa", tags=["mfa"])
api_router.include_router(session_router, prefix="/auth/sessions", tags=["sessions"])
api_router.include_router(consent_router, prefix="/auth/consent", tags=["consent"])
api_router.include_router(audit_router, prefix="/auth/audit", tags=["audit-logging"])
api_router.include_router(profile_router, prefix="/profiles", tags=["profiles"])
api_router.include_router(jobs_router, prefix="/jobs", tags=["jobs"])
api_router.include_router(matching_router, prefix="/matches", tags=["matching"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
api_router.include_router(payments_router, prefix="/payments", tags=["payments"])
from app.execution.routes import router as execution_router
from app.vault.routes import router as vault_router
from app.audit.routes import router as audit_router
from app.learning.routes import router as learning_router

api_router.include_router(execution_router, prefix="/execution", tags=["execution"])
api_router.include_router(vault_router, prefix="/vault", tags=["vault"])
api_router.include_router(audit_router, prefix="/audit", tags=["audit"])
api_router.include_router(learning_router, prefix="/learning", tags=["learning"])
api_router.include_router(ingestion_router, prefix="/ingestion", tags=["ingestion"])
api_router.include_router(enrichment_router, prefix="/enrichment", tags=["enrichment"])