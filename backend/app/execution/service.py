"""Execution service with state machine, provider adapters, and reconciliation."""
import uuid
from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.execution.models import ExecutionRequest, ExecutionResult, ReconciliationRecord
from app.execution.state_machine import can_transition, get_valid_transitions, is_terminal
from app.payments.provider import MockPSP

psp = MockPSP()

MAX_RETRIES = 3

def create_execution(db: Session, *, entity_id: str, execution_type: str, amount_cents: int, currency: str = "ZAR", payload: dict | None = None, decision_id: str | None = None, authorization_id: str | None = None, idempotency_key: str | None = None) -> ExecutionRequest:
    if idempotency_key:
        existing = db.query(ExecutionRequest).filter(ExecutionRequest.idempotency_key == idempotency_key).first()
        if existing:
            return existing
    request = ExecutionRequest(
        id=str(uuid.uuid4()),
        entity_id=entity_id,
        execution_type=execution_type,
        status="simulated",
        amount_cents=amount_cents,
        currency=currency,
        payload=payload or {},
        idempotency_key=idempotency_key,
        decision_id=decision_id,
        authorization_id=authorization_id,
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request

def advance_execution(db: Session, request_id: str, target_status: str, *, provider_ref: str | None = None, error_message: str | None = None, provider_response: dict | None = None) -> ExecutionRequest:
    request = db.query(ExecutionRequest).filter(ExecutionRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Execution request not found")
    if not can_transition(request.status, target_status):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Cannot transition from {request.status} to {target_status}")
    if is_terminal(request.status):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Execution already in terminal state")

    request.status = target_status
    request.updated_at = datetime.now(timezone.utc)
    if provider_ref:
        request.provider_ref = provider_ref
    if error_message:
        request.error_message = error_message

    result = ExecutionResult(
        id=str(uuid.uuid4()),
        request_id=request.id,
        status=target_status,
        provider_ref=provider_ref,
        provider_response=provider_response or {},
    )
    db.add(result)
    db.commit()
    db.refresh(request)
    return request

def submit_to_provider(db: Session, request_id: str) -> ExecutionRequest:
    request = db.query(ExecutionRequest).filter(ExecutionRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Execution request not found")
    if request.retry_count >= MAX_RETRIES:
        return advance_execution(db, request_id, "failed", error_message="Max retries exceeded")
    request.retry_count += 1
    if request.execution_type == "payout":
        result = psp.create_payout(request.amount_cents, reference=request.entity_id)
    elif request.execution_type == "cashout":
        result = psp.create_cashout(request.amount_cents)
    else:
        result = psp.create_funding(request.amount_cents, reference=request.entity_id)
    return advance_execution(db, request_id, "submitted", provider_ref=result.provider_ref, provider_response={"status": result.status})

def reconcile(db: Session, execution_id: str, new_status: str, notes: str = "", reconciled_by: str = "system") -> ReconciliationRecord:
    request = db.query(ExecutionRequest).filter(ExecutionRequest.id == execution_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Execution request not found")
    old_status = request.status
    record = ReconciliationRecord(
        id=str(uuid.uuid4()),
        execution_id=execution_id,
        status_before=old_status,
        status_after=new_status,
        notes=notes,
        reconciled_by=reconciled_by,
    )
    db.add(record)
    request.status = new_status
    request.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(record)
    return record
