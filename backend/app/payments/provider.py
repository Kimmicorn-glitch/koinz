import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass(frozen=True)
class FundingResult:
    provider_ref: str
    status: str


@dataclass(frozen=True)
class PayoutResult:
    provider_ref: str
    status: str


@dataclass(frozen=True)
class CashoutResult:
    provider_ref: str
    status: str
    voucher_code: str
    expires_at: datetime


class MockPSP:
    def create_funding(self, amount_cents: int, reference: str | None) -> FundingResult:
        provider_ref = f"fund_{secrets.token_hex(6)}"
        return FundingResult(provider_ref=provider_ref, status="succeeded")

    def create_payout(self, amount_cents: int, reference: str | None) -> PayoutResult:
        provider_ref = f"payout_{secrets.token_hex(6)}"
        return PayoutResult(provider_ref=provider_ref, status="processing")

    def create_cashout(self, amount_cents: int) -> CashoutResult:
        provider_ref = f"cash_{secrets.token_hex(6)}"
        voucher_code = f"VX-{secrets.token_hex(4)}"
        expires_at = datetime.now(timezone.utc) + timedelta(hours=2)
        return CashoutResult(provider_ref=provider_ref, status="active", voucher_code=voucher_code, expires_at=expires_at)

