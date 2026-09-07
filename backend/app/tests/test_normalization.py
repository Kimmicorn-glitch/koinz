from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.connectors.contracts import NormalizedTransaction
from app.connectors.normalization import normalize_transaction
from app.domain.transactions import CanonicalTransaction, TransactionStatus


def test_normalization_is_stable_and_provider_neutral() -> None:
    source = NormalizedTransaction(
        provider="bank-a",
        external_id="txn-1",
        account_external_id="acct-1",
        subject_id="user-1",
        amount=Decimal("10.00"),
        currency="zar",
        occurred_at=datetime(2026, 1, 1, 12, tzinfo=timezone.utc),
        direction="DEBIT",
        status="SETTLED",
        description="Test purchase",
    )

    first = normalize_transaction(source)
    second = normalize_transaction(source)

    assert first == second
    assert first.transaction_id == CanonicalTransaction.stable_id("bank-a", "txn-1")
    assert first.currency == "ZAR"
    assert first.status is TransactionStatus.SETTLED
    assert first.occurred_at.tzinfo == timezone.utc


def test_normalization_rejects_unknown_status() -> None:
    source = NormalizedTransaction(
        provider="bank-a",
        external_id="txn-1",
        account_external_id="acct-1",
        subject_id="user-1",
        amount=Decimal("10.00"),
        currency="ZAR",
        occurred_at=datetime.now(timezone.utc),
        direction="credit",
        status="completed-but-unknown",
    )

    with pytest.raises(ValueError, match="Unsupported transaction status"):
        normalize_transaction(source)
