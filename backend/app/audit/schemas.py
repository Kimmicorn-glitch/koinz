from pydantic import BaseModel, Field

class AuditEventCreate(BaseModel):
    correlation_id: str
    event_type: str
    entity_type: str
    entity_id: str
    actor_id: str = "system"
    payload: dict = Field(default_factory=dict)

class AuditEventOut(BaseModel):
    id: str
    correlation_id: str
    event_type: str
    entity_type: str
    entity_id: str
    actor_id: str
    sequence_number: int
    event_hash: str
    created_at: str

class HashChainVerification(BaseModel):
    valid: bool
    events_checked: int
    break_at: int | None = None
    tampered_at: int | None = None

class TransactionReport(BaseModel):
    total_transactions: int
    by_type: dict
    generated_at: str
