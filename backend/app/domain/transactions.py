"""Canonical transaction model used by downstream risk and policy flows."""

from datetime import datetime, timezone
from decimal import Decimal
from enum import StrEnum
from hashlib import sha256

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TransactionDirection(StrEnum):
    CREDIT = "credit"
    DEBIT = "debit"


class TransactionStatus(StrEnum):
    PENDING = "pending"
    SETTLED = "settled"
    FAILED = "failed"
    REVERSED = "reversed"
    UNKNOWN = "unknown"


class CanonicalTransaction(BaseModel):
    """Stable, provider-neutral transaction record.

    The model intentionally contains no raw provider payload or credentials.
    ``transaction_id`` is deterministic for a provider/external-id pair so
    repeated ingestion is idempotent.
    """

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    transaction_id: str = Field(min_length=16, max_length=64)
    source: str = Field(min_length=1, max_length=64)
    external_id: str = Field(min_length=1, max_length=255)
    subject_id: str = Field(min_length=1, max_length=64)
    account_external_id: str = Field(min_length=1, max_length=255)
    amount: Decimal = Field(gt=Decimal("0"), max_digits=20, decimal_places=4)
    currency: str = Field(min_length=3, max_length=3)
    occurred_at: datetime
    direction: TransactionDirection
    status: TransactionStatus
    description: str | None = Field(default=None, max_length=500)

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        value = value.upper()
        if not value.isalpha():
            raise ValueError("currency must be an ISO alphabetic code")
        return value

    @field_validator("occurred_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("occurred_at must include a timezone")
        return value.astimezone(timezone.utc)

    @staticmethod
    def stable_id(source: str, external_id: str) -> str:
        identity = f"{source}\x00{external_id}".encode("utf-8")
        return sha256(identity).hexdigest()
