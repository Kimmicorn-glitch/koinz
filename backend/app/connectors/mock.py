"""Deterministic local connectors; never use these for real money movement."""

from datetime import datetime, timezone
from decimal import Decimal

from app.connectors.contracts import (
    ConnectorContext,
    EventType,
    InstrumentType,
    NormalizedAccount,
    NormalizedBeneficiary,
    NormalizedEvent,
    NormalizedInvestment,
    NormalizedMandate,
    NormalizedTransaction,
    PaymentRequest,
    PaymentResult,
    WalletBalance,
)


class MockFinancialDataConnector:
    provider = "mock"

    def list_accounts(self, context: ConnectorContext) -> list[NormalizedAccount]:
        return [
            NormalizedAccount(
                provider=self.provider,
                external_id=f"acct_{context.subject_id}",
                subject_id=context.subject_id,
                instrument_type=InstrumentType.BANK_ACCOUNT,
                currency="ZAR",
                status="active",
                last4="0001",
            )
        ]

    def list_transactions(self, context: ConnectorContext, account_external_id: str) -> list[NormalizedTransaction]:
        return [
            NormalizedTransaction(
                provider=self.provider,
                external_id=f"txn_{context.subject_id}_001",
                account_external_id=account_external_id,
                subject_id=context.subject_id,
                amount=Decimal("100.00"),
                currency="ZAR",
                occurred_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
                direction="credit",
                status="settled",
                description="Local test transaction",
            )
        ]

    def list_investments(self, context: ConnectorContext) -> list[NormalizedInvestment]:
        return [
            NormalizedInvestment(
                provider=self.provider,
                external_id=f"position_{context.subject_id}_001",
                subject_id=context.subject_id,
                symbol="TEST",
                quantity=Decimal("1"),
                market_value=Decimal("100.00"),
                currency="ZAR",
            )
        ]

    def list_events(self, context: ConnectorContext, since: datetime | None = None) -> list[NormalizedEvent]:
        event = NormalizedEvent(
            provider=self.provider,
            external_id=f"event_{context.subject_id}_001",
            subject_id=context.subject_id,
            event_type=EventType.ACCOUNT,
            occurred_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            action="account_viewed",
            source="mock",
            metadata={"environment": "test"},
        )
        return [event] if since is None or event.occurred_at > since else []

    def list_beneficiaries(self, context: ConnectorContext) -> list[NormalizedBeneficiary]:
        return [NormalizedBeneficiary(self.provider, f"ben_{context.subject_id}_001", context.subject_id, "Test beneficiary", "active")]

    def list_mandates(self, context: ConnectorContext) -> list[NormalizedMandate]:
        return [NormalizedMandate(self.provider, f"mandate_{context.subject_id}_001", context.subject_id, "Test counterparty", "active", Decimal("500.00"), "ZAR")]

    def list_wallets(self, context: ConnectorContext) -> list[WalletBalance]:
        return [WalletBalance(self.provider, f"wallet_{context.subject_id}", context.subject_id, Decimal("0.00"), "ZAR")]


class MockPaymentConnector:
    provider = "mock"

    def submit_payment(self, context: ConnectorContext, request: PaymentRequest) -> PaymentResult:
        return PaymentResult(
            provider=self.provider,
            external_id=f"payment_{context.subject_id}_{request.idempotency_key}",
            status="SIMULATED",
            provider_reference=None,
        )
