from datetime import datetime

from pydantic import BaseModel, Field


class WalletOut(BaseModel):
    id: str
    user_id: str
    currency: str
    balance_cents: int


class LedgerEntryOut(BaseModel):
    id: str
    wallet_id: str
    direction: str
    kind: str
    amount_cents: int
    status: str
    reference: str | None
    created_at: datetime


class FundEmployerRequest(BaseModel):
    amount_cents: int = Field(..., gt=0)
    reference: str | None = None


class FundEmployerResponse(BaseModel):
    funding_id: str
    status: str
    wallet_balance_cents: int


class PayWorkerRequest(BaseModel):
    worker_id: str
    amount_cents: int = Field(..., gt=0)
    reference: str | None = None


class PayWorkerResponse(BaseModel):
    transfer_id: str
    employer_balance_cents: int


class BankAccountCreate(BaseModel):
    bank_name: str
    account_holder: str
    account_number_last4: str = Field(..., min_length=4, max_length=4)


class BankAccountOut(BaseModel):
    id: str
    bank_name: str
    account_holder: str
    account_number_last4: str
    verified: bool


class PayoutRequest(BaseModel):
    bank_account_id: str
    amount_cents: int = Field(..., gt=0)


class PayoutResponse(BaseModel):
    payout_id: str
    status: str
    provider_ref: str | None
    wallet_balance_cents: int


class CashoutRequest(BaseModel):
    amount_cents: int = Field(..., gt=0)


class CashoutResponse(BaseModel):
    cashout_id: str
    status: str
    voucher_code_masked: str
    expires_at: datetime
    wallet_balance_cents: int


class TransactionList(BaseModel):
    items: list[LedgerEntryOut]

