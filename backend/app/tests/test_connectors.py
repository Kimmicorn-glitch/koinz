from datetime import datetime, timezone
from decimal import Decimal

from app.connectors.contracts import ConnectorContext, InstrumentType, PaymentRequest
from app.connectors.mock import MockFinancialDataConnector, MockPaymentConnector


def test_mock_connector_returns_provider_neutral_records() -> None:
    context = ConnectorContext(subject_id="user-1", correlation_id="corr-1")
    connector = MockFinancialDataConnector()

    accounts = connector.list_accounts(context)
    transactions = connector.list_transactions(context, accounts[0].external_id)

    assert accounts[0].instrument_type is InstrumentType.BANK_ACCOUNT
    assert transactions[0].amount == Decimal("100.00")
    assert transactions[0].occurred_at.tzinfo == timezone.utc
    assert accounts[0].provider == "mock"


def test_mock_payment_can_only_simulate() -> None:
    context = ConnectorContext(subject_id="user-1", correlation_id="corr-1")
    request = PaymentRequest("user-1", Decimal("10.00"), "ZAR", "beneficiary-1", "idem-1")

    result = MockPaymentConnector().submit_payment(context, request)

    assert result.status == "SIMULATED"
    assert result.provider_reference is None
