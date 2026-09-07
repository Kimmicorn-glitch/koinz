from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.core.security import Roles, require_roles
from app.db.session import get_db
from app.payments.models import BankAccount
from app.payments.schemas import (
    BankAccountCreate,
    BankAccountOut,
    CashoutRequest,
    CashoutResponse,
    FundEmployerRequest,
    FundEmployerResponse,
    LedgerEntryOut,
    PayWorkerRequest,
    PayWorkerResponse,
    PayoutRequest,
    PayoutResponse,
    TransactionList,
    WalletOut,
)
from app.payments.service import (
    add_bank_account,
    cashout_atm,
    fund_employer,
    get_or_create_wallet,
    list_transactions,
    pay_worker,
    payout_to_bank,
)

router = APIRouter()


@router.get("/employer/wallet", response_model=WalletOut)
def employer_wallet(
    user: dict = Depends(require_roles({Roles.EMPLOYER, Roles.ADMIN})), db: Session = Depends(get_db)
) -> WalletOut:
    wallet = get_or_create_wallet(db, user_id=user["id"], role=user["role"])
    return WalletOut(id=wallet.id, user_id=wallet.user_id, currency=wallet.currency, balance_cents=wallet.balance_cents)


@router.post("/employer/fund", response_model=FundEmployerResponse)
def employer_fund(
    payload: FundEmployerRequest,
    user: dict = Depends(require_roles({Roles.EMPLOYER, Roles.ADMIN})),
    db: Session = Depends(get_db),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> FundEmployerResponse:
    response = fund_employer(
        db,
        employer_id=user["id"],
        amount_cents=payload.amount_cents,
        reference=payload.reference,
        idempotency_key=idempotency_key,
    )
    return FundEmployerResponse(**response)


@router.post("/employer/pay-worker", response_model=PayWorkerResponse)
def employer_pay_worker(
    payload: PayWorkerRequest,
    user: dict = Depends(require_roles({Roles.EMPLOYER, Roles.ADMIN})),
    db: Session = Depends(get_db),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> PayWorkerResponse:
    response = pay_worker(
        db,
        employer_id=user["id"],
        worker_id=payload.worker_id,
        amount_cents=payload.amount_cents,
        reference=payload.reference,
        idempotency_key=idempotency_key,
    )
    return PayWorkerResponse(**response)


@router.get("/worker/wallet", response_model=WalletOut)
def worker_wallet(
    user: dict = Depends(require_roles({Roles.WORKER, Roles.ADMIN})), db: Session = Depends(get_db)
) -> WalletOut:
    wallet = get_or_create_wallet(db, user_id=user["id"], role=user["role"])
    return WalletOut(id=wallet.id, user_id=wallet.user_id, currency=wallet.currency, balance_cents=wallet.balance_cents)


@router.get("/worker/transactions", response_model=TransactionList)
def worker_transactions(
    user: dict = Depends(require_roles({Roles.WORKER, Roles.ADMIN})), db: Session = Depends(get_db)
) -> TransactionList:
    wallet = get_or_create_wallet(db, user_id=user["id"], role=user["role"])
    items = [
        LedgerEntryOut(
            id=entry.id,
            wallet_id=entry.wallet_id,
            direction=entry.direction,
            kind=entry.kind,
            amount_cents=entry.amount_cents,
            status=entry.status,
            reference=entry.reference,
            created_at=entry.created_at,
        )
        for entry in list_transactions(db, wallet_id=wallet.id)
    ]
    return TransactionList(items=items)


@router.get("/worker/bank-accounts", response_model=list[BankAccountOut])
def worker_bank_accounts(
    user: dict = Depends(require_roles({Roles.WORKER, Roles.ADMIN})), db: Session = Depends(get_db)
) -> list[BankAccountOut]:
    accounts = db.query(BankAccount).filter_by(user_id=user["id"]).all()
    return [
        BankAccountOut(
            id=account.id,
            bank_name=account.bank_name,
            account_holder=account.account_holder,
            account_number_last4=account.account_number_last4,
            verified=account.verified,
        )
        for account in accounts
    ]


@router.post("/worker/bank-accounts", response_model=BankAccountOut)
def worker_add_bank_account(
    payload: BankAccountCreate,
    user: dict = Depends(require_roles({Roles.WORKER, Roles.ADMIN})),
    db: Session = Depends(get_db),
) -> BankAccountOut:
    account = add_bank_account(
        db,
        user_id=user["id"],
        bank_name=payload.bank_name,
        account_holder=payload.account_holder,
        account_number_last4=payload.account_number_last4,
    )
    return BankAccountOut(
        id=account.id,
        bank_name=account.bank_name,
        account_holder=account.account_holder,
        account_number_last4=account.account_number_last4,
        verified=account.verified,
    )


@router.post("/worker/payout", response_model=PayoutResponse)
def worker_payout(
    payload: PayoutRequest,
    user: dict = Depends(require_roles({Roles.WORKER, Roles.ADMIN})),
    db: Session = Depends(get_db),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> PayoutResponse:
    response = payout_to_bank(
        db,
        worker_id=user["id"],
        bank_account_id=payload.bank_account_id,
        amount_cents=payload.amount_cents,
        idempotency_key=idempotency_key,
    )
    return PayoutResponse(**response)


@router.post("/worker/cashout", response_model=CashoutResponse)
def worker_cashout(
    payload: CashoutRequest,
    user: dict = Depends(require_roles({Roles.WORKER, Roles.ADMIN})),
    db: Session = Depends(get_db),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> CashoutResponse:
    response = cashout_atm(
        db,
        worker_id=user["id"],
        amount_cents=payload.amount_cents,
        idempotency_key=idempotency_key,
    )
    return CashoutResponse(**response)

