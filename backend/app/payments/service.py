import hashlib
import json
import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import Roles
from app.payments.models import (
    BankAccount,
    CashoutVoucher,
    EmployerFunding,
    LedgerEntry,
    PaymentIdempotency,
    Wallet,
    WorkerPayout,
)
from app.payments.provider import MockPSP

psp = MockPSP()


def _hash_request(payload: dict) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _get_idempotent_response(
    db: Session, *, user_id: str, key: str, endpoint: str, request_hash: str
) -> dict | None:
    existing = (
        db.query(PaymentIdempotency)
        .filter(
            PaymentIdempotency.user_id == user_id,
            PaymentIdempotency.key == key,
            PaymentIdempotency.endpoint == endpoint,
        )
        .first()
    )
    if existing is None:
        return None
    if existing.request_hash != request_hash:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Idempotency key reused with new payload")
    return existing.response_json


def _store_idempotent_response(
    db: Session, *, user_id: str, key: str, endpoint: str, request_hash: str, response: dict
) -> None:
    db.add(
        PaymentIdempotency(
            id=str(uuid.uuid4()),
            user_id=user_id,
            key=key,
            endpoint=endpoint,
            request_hash=request_hash,
            response_json=response,
        )
    )


def get_or_create_wallet(db: Session, *, user_id: str, role: str) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if wallet:
        return wallet
    wallet = Wallet(id=str(uuid.uuid4()), user_id=user_id, role=role, balance_cents=0, currency="ZAR")
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return wallet


def list_transactions(db: Session, *, wallet_id: str, limit: int = 50) -> list[LedgerEntry]:
    return (
        db.query(LedgerEntry)
        .filter(LedgerEntry.wallet_id == wallet_id)
        .order_by(LedgerEntry.created_at.desc())
        .limit(limit)
        .all()
    )


def _add_ledger(
    db: Session, *, wallet_id: str, direction: str, kind: str, amount_cents: int, reference: str | None, metadata: dict
) -> LedgerEntry:
    entry = LedgerEntry(
        id=str(uuid.uuid4()),
        wallet_id=wallet_id,
        direction=direction,
        kind=kind,
        amount_cents=amount_cents,
        status="settled",
        reference=reference,
        meta=metadata,
        created_at=datetime.now(timezone.utc),
    )
    db.add(entry)
    return entry


def fund_employer(
    db: Session, *, employer_id: str, amount_cents: int, reference: str | None, idempotency_key: str | None
) -> dict:
    request_payload = {"amount_cents": amount_cents, "reference": reference}
    if idempotency_key:
        request_hash = _hash_request(request_payload)
        existing = _get_idempotent_response(
            db, user_id=employer_id, key=idempotency_key, endpoint="fund_employer", request_hash=request_hash
        )
        if existing:
            return existing

    wallet = get_or_create_wallet(db, user_id=employer_id, role=Roles.EMPLOYER)
    result = psp.create_funding(amount_cents, reference)
    funding = EmployerFunding(
        id=str(uuid.uuid4()),
        employer_id=employer_id,
        amount_cents=amount_cents,
        status=result.status,
        provider_ref=result.provider_ref,
    )
    db.add(funding)
    wallet.balance_cents += amount_cents
    _add_ledger(
        db,
        wallet_id=wallet.id,
        direction="credit",
        kind="funding",
        amount_cents=amount_cents,
        reference=reference,
        metadata={"provider_ref": result.provider_ref},
    )

    response = {"funding_id": funding.id, "status": funding.status, "wallet_balance_cents": wallet.balance_cents}
    if idempotency_key:
        _store_idempotent_response(
            db,
            user_id=employer_id,
            key=idempotency_key,
            endpoint="fund_employer",
            request_hash=_hash_request(request_payload),
            response=response,
        )
    db.commit()
    return response


def pay_worker(
    db: Session,
    *,
    employer_id: str,
    worker_id: str,
    amount_cents: int,
    reference: str | None,
    idempotency_key: str | None,
) -> dict:
    request_payload = {"worker_id": worker_id, "amount_cents": amount_cents, "reference": reference}
    if idempotency_key:
        request_hash = _hash_request(request_payload)
        existing = _get_idempotent_response(
            db, user_id=employer_id, key=idempotency_key, endpoint="pay_worker", request_hash=request_hash
        )
        if existing:
            return existing

    employer_wallet = get_or_create_wallet(db, user_id=employer_id, role=Roles.EMPLOYER)
    worker_wallet = get_or_create_wallet(db, user_id=worker_id, role=Roles.WORKER)
    if employer_wallet.balance_cents < amount_cents:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient employer balance")

    employer_wallet.balance_cents -= amount_cents
    worker_wallet.balance_cents += amount_cents

    transfer_id = str(uuid.uuid4())
    _add_ledger(
        db,
        wallet_id=employer_wallet.id,
        direction="debit",
        kind="transfer",
        amount_cents=amount_cents,
        reference=reference,
        metadata={"transfer_id": transfer_id, "counterparty": worker_id},
    )
    _add_ledger(
        db,
        wallet_id=worker_wallet.id,
        direction="credit",
        kind="transfer",
        amount_cents=amount_cents,
        reference=reference,
        metadata={"transfer_id": transfer_id, "counterparty": employer_id},
    )

    response = {"transfer_id": transfer_id, "employer_balance_cents": employer_wallet.balance_cents}
    if idempotency_key:
        _store_idempotent_response(
            db,
            user_id=employer_id,
            key=idempotency_key,
            endpoint="pay_worker",
            request_hash=_hash_request(request_payload),
            response=response,
        )
    db.commit()
    return response


def add_bank_account(
    db: Session, *, user_id: str, bank_name: str, account_holder: str, account_number_last4: str
) -> BankAccount:
    account = BankAccount(
        id=str(uuid.uuid4()),
        user_id=user_id,
        bank_name=bank_name,
        account_holder=account_holder,
        account_number_last4=account_number_last4,
        verified=True,
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def payout_to_bank(
    db: Session,
    *,
    worker_id: str,
    bank_account_id: str,
    amount_cents: int,
    idempotency_key: str | None,
) -> dict:
    request_payload = {"bank_account_id": bank_account_id, "amount_cents": amount_cents}
    if idempotency_key:
        request_hash = _hash_request(request_payload)
        existing = _get_idempotent_response(
            db, user_id=worker_id, key=idempotency_key, endpoint="payout", request_hash=request_hash
        )
        if existing:
            return existing

    account = db.query(BankAccount).filter(BankAccount.id == bank_account_id, BankAccount.user_id == worker_id).first()
    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bank account not found")
    if not account.verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bank account not verified")

    wallet = get_or_create_wallet(db, user_id=worker_id, role=Roles.WORKER)
    if wallet.balance_cents < amount_cents:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient wallet balance")

    result = psp.create_payout(amount_cents, reference=account.id)
    payout = WorkerPayout(
        id=str(uuid.uuid4()),
        worker_id=worker_id,
        bank_account_id=account.id,
        amount_cents=amount_cents,
        status=result.status,
        provider_ref=result.provider_ref,
    )
    db.add(payout)
    wallet.balance_cents -= amount_cents
    _add_ledger(
        db,
        wallet_id=wallet.id,
        direction="debit",
        kind="payout",
        amount_cents=amount_cents,
        reference=account.id,
        metadata={"provider_ref": result.provider_ref},
    )

    response = {
        "payout_id": payout.id,
        "status": payout.status,
        "provider_ref": payout.provider_ref,
        "wallet_balance_cents": wallet.balance_cents,
    }
    if idempotency_key:
        _store_idempotent_response(
            db,
            user_id=worker_id,
            key=idempotency_key,
            endpoint="payout",
            request_hash=_hash_request(request_payload),
            response=response,
        )
    db.commit()
    return response


def cashout_atm(db: Session, *, worker_id: str, amount_cents: int, idempotency_key: str | None) -> dict:
    request_payload = {"amount_cents": amount_cents}
    if idempotency_key:
        request_hash = _hash_request(request_payload)
        existing = _get_idempotent_response(
            db, user_id=worker_id, key=idempotency_key, endpoint="cashout", request_hash=request_hash
        )
        if existing:
            return existing

    wallet = get_or_create_wallet(db, user_id=worker_id, role=Roles.WORKER)
    if wallet.balance_cents < amount_cents:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient wallet balance")

    result = psp.create_cashout(amount_cents)
    cashout = CashoutVoucher(
        id=str(uuid.uuid4()),
        worker_id=worker_id,
        amount_cents=amount_cents,
        status=result.status,
        voucher_code_masked=f"{result.voucher_code[:4]}****{result.voucher_code[-2:]}",
        expires_at=result.expires_at,
        provider_ref=result.provider_ref,
    )
    db.add(cashout)
    wallet.balance_cents -= amount_cents
    _add_ledger(
        db,
        wallet_id=wallet.id,
        direction="debit",
        kind="cashout",
        amount_cents=amount_cents,
        reference=cashout.id,
        metadata={"provider_ref": result.provider_ref},
    )

    response = {
        "cashout_id": cashout.id,
        "status": cashout.status,
        "voucher_code_masked": cashout.voucher_code_masked,
        "expires_at": cashout.expires_at,
        "wallet_balance_cents": wallet.balance_cents,
    }
    if idempotency_key:
        _store_idempotent_response(
            db,
            user_id=worker_id,
            key=idempotency_key,
            endpoint="cashout",
            request_hash=_hash_request(request_payload),
            response=response,
        )
    db.commit()
    return response

