from pydantic import BaseModel, Field

class ExecutionRequestCreate(BaseModel):
    entity_id: str
    execution_type: str
    amount_cents: int = Field(ge=0)
    currency: str = Field(default="ZAR", max_length=8)
    payload: dict = Field(default_factory=dict)
    decision_id: str | None = None
    authorization_id: str | None = None
    idempotency_key: str | None = None

class ExecutionRequestOut(BaseModel):
    id: str
    entity_id: str
    execution_type: str
    status: str
    amount_cents: int
    currency: str
    provider_ref: str | None
    retry_count: int
    error_message: str | None
    created_at: str
    updated_at: str

class ExecutionAdvanceRequest(BaseModel):
    target_status: str
    provider_ref: str | None = None
    error_message: str | None = None

class ReconciliationRequest(BaseModel):
    new_status: str = Field(pattern=r"^(settled|failed)$")
    notes: str = Field(default="", max_length=500)

class ReconciliationOut(BaseModel):
    id: str
    execution_id: str
    status_before: str
    status_after: str
    notes: str
    reconciled_by: str
