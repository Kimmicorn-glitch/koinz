from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession
from app.core.security import Roles, require_roles
from app.db.session import get_db
from app.ingestion.schemas import AccountIngest, TransactionIngest, BeneficiaryIngest, MandateIngest, IngestedRecordOut
from app.ingestion.service import ingest_account, ingest_transaction, ingest_beneficiary, ingest_mandate

router = APIRouter()

@router.post("/accounts", response_model=IngestedRecordOut)
def ingest_accounts(payload: AccountIngest, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    record = ingest_account(db, payload.model_dump(), source=payload.source)
    return IngestedRecordOut(id=record.id, external_id=record.external_id, source=record.source, schema_version=record.schema_version, provenance=record.provenance)

@router.post("/transactions", response_model=IngestedRecordOut)
def ingest_transactions(payload: TransactionIngest, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    record = ingest_transaction(db, payload.model_dump(), source=payload.source)
    return IngestedRecordOut(id=record.id, external_id=record.external_id, source=record.source, schema_version=record.schema_version, provenance=record.provenance)

@router.post("/beneficiaries", response_model=IngestedRecordOut)
def ingest_beneficiaries(payload: BeneficiaryIngest, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    record = ingest_beneficiary(db, payload.model_dump(), source=payload.source)
    return IngestedRecordOut(id=record.id, external_id=record.external_id, source=record.source, schema_version=record.schema_version, provenance=record.provenance)

@router.post("/mandates", response_model=IngestedRecordOut)
def ingest_mandates(payload: MandateIngest, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    record = ingest_mandate(db, payload.model_dump(), source=payload.source)
    return IngestedRecordOut(id=record.id, external_id=record.external_id, source=record.source, schema_version=record.schema_version, provenance=record.provenance)