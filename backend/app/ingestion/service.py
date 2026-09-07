"""Ingestion service with duplicate detection and provenance tracking."""
import hashlib
import json
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.ingestion.models import IngestedAccount, IngestedTransaction, IngestedBeneficiary, IngestedMandate

def _compute_hash(data: dict) -> str:
    encoded = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()

def _provenance(source: str, data_hash: str) -> dict:
    return {
        "source": source,
        "data_hash": data_hash,
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "schema_version": 1,
    }

def ingest_account(db: Session, payload: dict, *, source: str) -> IngestedAccount:
    data_hash = _compute_hash(payload)
    existing = db.query(IngestedAccount).filter(
        IngestedAccount.external_id == payload["external_id"],
        IngestedAccount.source == source,
    ).first()
    if existing:
        existing.data = payload
        existing.provenance = _provenance(source, data_hash)
        db.commit()
        db.refresh(existing)
        return existing
    record = IngestedAccount(
        id=str(uuid.uuid4()),
        external_id=payload["external_id"],
        source=source,
        schema_version=payload.get("schema_version", 1),
        data=payload,
        provenance=_provenance(source, data_hash),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def ingest_transaction(db: Session, payload: dict, *, source: str) -> IngestedTransaction:
    data_hash = _compute_hash(payload)
    existing = db.query(IngestedTransaction).filter(
        IngestedTransaction.external_id == payload["external_id"],
        IngestedTransaction.source == source,
    ).first()
    if existing:
        existing.data = payload
        existing.provenance = _provenance(source, data_hash)
        db.commit()
        db.refresh(existing)
        return existing
    record = IngestedTransaction(
        id=str(uuid.uuid4()),
        external_id=payload["external_id"],
        source=source,
        schema_version=payload.get("schema_version", 1),
        data=payload,
        provenance=_provenance(source, data_hash),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def ingest_beneficiary(db: Session, payload: dict, *, source: str) -> IngestedBeneficiary:
    data_hash = _compute_hash(payload)
    existing = db.query(IngestedBeneficiary).filter(
        IngestedBeneficiary.external_id == payload["external_id"],
        IngestedBeneficiary.source == source,
    ).first()
    if existing:
        existing.data = payload
        existing.provenance = _provenance(source, data_hash)
        db.commit()
        db.refresh(existing)
        return existing
    record = IngestedBeneficiary(
        id=str(uuid.uuid4()),
        external_id=payload["external_id"],
        source=source,
        schema_version=payload.get("schema_version", 1),
        data=payload,
        provenance=_provenance(source, data_hash),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def ingest_mandate(db: Session, payload: dict, *, source: str) -> IngestedMandate:
    data_hash = _compute_hash(payload)
    existing = db.query(IngestedMandate).filter(
        IngestedMandate.external_id == payload["external_id"],
        IngestedMandate.source == source,
    ).first()
    if existing:
        existing.data = payload
        existing.provenance = _provenance(source, data_hash)
        db.commit()
        db.refresh(existing)
        return existing
    record = IngestedMandate(
        id=str(uuid.uuid4()),
        external_id=payload["external_id"],
        source=source,
        schema_version=payload.get("schema_version", 1),
        data=payload,
        provenance=_provenance(source, data_hash),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record