from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession
from app.core.security import Roles, require_roles
from app.db.session import get_db
from app.execution.schemas import ExecutionRequestCreate, ExecutionRequestOut, ExecutionAdvanceRequest, ReconciliationRequest, ReconciliationOut
from app.execution.service import create_execution, advance_execution, submit_to_provider, reconcile
from app.execution.state_machine import get_valid_transitions, is_terminal

router = APIRouter()

@router.post("/", response_model=ExecutionRequestOut)
def create_exec(payload: ExecutionRequestCreate, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    r = create_execution(db, entity_id=payload.entity_id, execution_type=payload.execution_type, amount_cents=payload.amount_cents, currency=payload.currency, payload=payload.payload, decision_id=payload.decision_id, authorization_id=payload.authorization_id, idempotency_key=payload.idempotency_key)
    return ExecutionRequestOut(id=r.id, entity_id=r.entity_id, execution_type=r.execution_type, status=r.status, amount_cents=r.amount_cents, currency=r.currency, provider_ref=r.provider_ref, retry_count=r.retry_count, error_message=r.error_message, created_at=str(r.created_at), updated_at=str(r.updated_at))

@router.get("/{request_id}", response_model=ExecutionRequestOut)
def get_exec(request_id: str, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    from app.execution.models import ExecutionRequest
    r = db.query(ExecutionRequest).filter(ExecutionRequest.id == request_id).first()
    if not r:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not found")
    return ExecutionRequestOut(id=r.id, entity_id=r.entity_id, execution_type=r.execution_type, status=r.status, amount_cents=r.amount_cents, currency=r.currency, provider_ref=r.provider_ref, retry_count=r.retry_count, error_message=r.error_message, created_at=str(r.created_at), updated_at=str(r.updated_at))

@router.get("/{request_id}/transitions")
def transitions(request_id: str, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    from app.execution.models import ExecutionRequest
    r = db.query(ExecutionRequest).filter(ExecutionRequest.id == request_id).first()
    if not r:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not found")
    return {"current": r.status, "valid_transitions": get_valid_transitions(r.status), "terminal": is_terminal(r.status)}

@router.post("/{request_id}/advance", response_model=ExecutionRequestOut)
def advance(request_id: str, payload: ExecutionAdvanceRequest, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    r = advance_execution(db, request_id, payload.target_status, provider_ref=payload.provider_ref, error_message=payload.error_message)
    return ExecutionRequestOut(id=r.id, entity_id=r.entity_id, execution_type=r.execution_type, status=r.status, amount_cents=r.amount_cents, currency=r.currency, provider_ref=r.provider_ref, retry_count=r.retry_count, error_message=r.error_message, created_at=str(r.created_at), updated_at=str(r.updated_at))

@router.post("/{request_id}/submit", response_model=ExecutionRequestOut)
def submit(request_id: str, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    r = submit_to_provider(db, request_id)
    return ExecutionRequestOut(id=r.id, entity_id=r.entity_id, execution_type=r.execution_type, status=r.status, amount_cents=r.amount_cents, currency=r.currency, provider_ref=r.provider_ref, retry_count=r.retry_count, error_message=r.error_message, created_at=str(r.created_at), updated_at=str(r.updated_at))

@router.post("/{request_id}/reconcile", response_model=ReconciliationOut)
def reconcile_exec(request_id: str, payload: ReconciliationRequest, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    r = reconcile(db, request_id, payload.new_status, notes=payload.notes, reconciled_by=user["id"])
    return ReconciliationOut(id=r.id, execution_id=r.execution_id, status_before=r.status_before, status_after=r.status_after, notes=r.notes, reconciled_by=r.reconciled_by)
