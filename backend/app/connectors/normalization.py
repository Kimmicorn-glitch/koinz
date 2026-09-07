"""Conversion from connector records to canonical domain records."""

from app.connectors.contracts import NormalizedTransaction
from app.domain.transactions import CanonicalTransaction, TransactionDirection, TransactionStatus


def normalize_transaction(record: NormalizedTransaction) -> CanonicalTransaction:
    """Normalize one connector result without carrying provider metadata through."""

    try:
        direction = TransactionDirection(record.direction.lower())
    except ValueError as exc:
        raise ValueError(f"Unsupported transaction direction: {record.direction}") from exc

    try:
        status = TransactionStatus(record.status.lower())
    except ValueError as exc:
        raise ValueError(f"Unsupported transaction status: {record.status}") from exc

    return CanonicalTransaction(
        transaction_id=CanonicalTransaction.stable_id(record.provider, record.external_id),
        source=record.provider,
        external_id=record.external_id,
        subject_id=record.subject_id,
        account_external_id=record.account_external_id,
        amount=record.amount,
        currency=record.currency,
        occurred_at=record.occurred_at,
        direction=direction,
        status=status,
        description=record.description,
    )
