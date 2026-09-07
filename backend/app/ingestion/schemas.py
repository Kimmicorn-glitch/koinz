"""Versioned Pydantic schemas for ingestion with strict validation."""
from pydantic import BaseModel, Field, field_validator

class AccountIngest(BaseModel):
    external_id: str = Field(min_length=1, max_length=255)
    source: str = Field(min_length=1, max_length=64)
    account_type: str = Field(min_length=1, max_length=32)
    currency: str = Field(min_length=3, max_length=3)
    holder_name: str = Field(min_length=1, max_length=200)
    metadata: dict = Field(default_factory=dict)
    schema_version: int = Field(default=1, ge=1, le=10)

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, v: str) -> str:
        return v.upper()

class TransactionIngest(BaseModel):
    external_id: str = Field(min_length=1, max_length=255)
    source: str = Field(min_length=1, max_length=64)
    account_external_id: str = Field(min_length=1, max_length=255)
    amount: float = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    direction: str = Field(pattern=r"^(credit|debit)$")
    description: str | None = Field(default=None, max_length=500)
    metadata: dict = Field(default_factory=dict)
    schema_version: int = Field(default=1, ge=1, le=10)

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, v: str) -> str:
        return v.upper()

class BeneficiaryIngest(BaseModel):
    external_id: str = Field(min_length=1, max_length=255)
    source: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=200)
    relationship: str = Field(min_length=1, max_length=64)
    verified: bool = Field(default=False)
    metadata: dict = Field(default_factory=dict)
    schema_version: int = Field(default=1, ge=1, le=10)

class MandateIngest(BaseModel):
    external_id: str = Field(min_length=1, max_length=255)
    source: str = Field(min_length=1, max_length=64)
    mandate_type: str = Field(min_length=1, max_length=64)
    amount_limit_cents: int = Field(ge=0)
    active: bool = Field(default=True)
    metadata: dict = Field(default_factory=dict)
    schema_version: int = Field(default=1, ge=1, le=10)

class IngestedRecordOut(BaseModel):
    id: str
    external_id: str
    source: str
    schema_version: int
    provenance: dict