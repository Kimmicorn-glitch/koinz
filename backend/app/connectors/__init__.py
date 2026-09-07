"""Provider-agnostic financial data connector contracts."""

from app.connectors.contracts import (
    AccountConnector,
    BeneficiaryConnector,
    ConnectorContext,
    EventConnector,
    InvestmentConnector,
    MandateConnector,
    PaymentConnector,
    TransactionConnector,
    WalletConnector,
)

__all__ = [
    "AccountConnector",
    "BeneficiaryConnector",
    "ConnectorContext",
    "EventConnector",
    "InvestmentConnector",
    "MandateConnector",
    "PaymentConnector",
    "TransactionConnector",
    "WalletConnector",
]
