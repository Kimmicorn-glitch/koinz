"""Stable connector contracts and normalized financial records.

Adapters translate provider-specific APIs into these records. Domain code
must depend on these contracts, never on a provider SDK or provider schema.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Protocol


class InstrumentType(StrEnum):
    BANK_ACCOUNT = "bank_account"
    CARD = "card"
    WALLET = "wallet"
    CRYPTO_ASSET = "crypto_asset"
    INVESTMENT = "investment"


class EventType(StrEnum):
    ACCOUNT = "account"
    DEVICE = "device"
    AUTHENTICATION = "authentication"
    BENEFICIARY = "beneficiary"
    MANDATE = "mandate"


@dataclass(frozen=True)
class ConnectorContext:
    """Request-scoped context; secrets stay inside the adapter boundary."""

    subject_id: str
    correlation_id: str


@dataclass(frozen=True)
class NormalizedAccount:
    provider: str
    external_id: str
    subject_id: str
    instrument_type: InstrumentType
    currency: str
    status: str
    last4: str | None = None


@dataclass(frozen=True)
class NormalizedTransaction:
    provider: str
    external_id: str
    account_external_id: str
    subject_id: str
    amount: Decimal
    currency: str
    occurred_at: datetime
    direction: str
    status: str
    description: str | None = None


@dataclass(frozen=True)
class NormalizedInvestment:
    provider: str
    external_id: str
    subject_id: str
    symbol: str
    quantity: Decimal
    market_value: Decimal
    currency: str


@dataclass(frozen=True)
class NormalizedEvent:
    provider: str
    external_id: str
    subject_id: str
    event_type: EventType
    occurred_at: datetime
    action: str
    source: str
    metadata: dict[str, str]


@dataclass(frozen=True)
class NormalizedBeneficiary:
    provider: str
    external_id: str
    subject_id: str
    display_name: str
    status: str


@dataclass(frozen=True)
class NormalizedMandate:
    provider: str
    external_id: str
    subject_id: str
    counterparty: str
    status: str
    maximum_amount: Decimal | None
    currency: str | None


@dataclass(frozen=True)
class PaymentRequest:
    subject_id: str
    amount: Decimal
    currency: str
    destination_external_id: str
    idempotency_key: str


@dataclass(frozen=True)
class PaymentResult:
    provider: str
    external_id: str
    status: str
    provider_reference: str | None


@dataclass(frozen=True)
class WalletBalance:
    provider: str
    external_id: str
    subject_id: str
    balance: Decimal
    currency: str


class AccountConnector(Protocol):
    def list_accounts(self, context: ConnectorContext) -> list[NormalizedAccount]: ...


class TransactionConnector(Protocol):
    def list_transactions(self, context: ConnectorContext, account_external_id: str) -> list[NormalizedTransaction]: ...


class InvestmentConnector(Protocol):
    def list_investments(self, context: ConnectorContext) -> list[NormalizedInvestment]: ...


class EventConnector(Protocol):
    def list_events(self, context: ConnectorContext, since: datetime | None = None) -> list[NormalizedEvent]: ...


class BeneficiaryConnector(Protocol):
    def list_beneficiaries(self, context: ConnectorContext) -> list[NormalizedBeneficiary]: ...


class MandateConnector(Protocol):
    def list_mandates(self, context: ConnectorContext) -> list[NormalizedMandate]: ...


class PaymentConnector(Protocol):
    def submit_payment(self, context: ConnectorContext, request: PaymentRequest) -> PaymentResult: ...


class WalletConnector(Protocol):
    def list_wallets(self, context: ConnectorContext) -> list[WalletBalance]: ...
