"""Vault service for field encryption, key rotation, retention, and deletion."""
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.core.crypto import encrypt_sensitive, decrypt_sensitive
from app.vault.models import EncryptedField, KeyRotationLog

def store_encrypted(db: Session, *, entity_id: str, field_name: str, plaintext: str, key_version: int = 1, expires_at: datetime | None = None) -> EncryptedField:
    existing = db.query(EncryptedField).filter(
        EncryptedField.entity_id == entity_id,
        EncryptedField.field_name == field_name,
        EncryptedField.deleted_at == None,
    ).first()
    encrypted = encrypt_sensitive(plaintext)
    if existing:
        existing.encrypted_value = encrypted
        existing.key_version = key_version
        db.commit()
        db.refresh(existing)
        return existing
    record = EncryptedField(
        id=str(uuid.uuid4()),
        entity_id=entity_id,
        field_name=field_name,
        encrypted_value=encrypted,
        key_version=key_version,
        expires_at=expires_at,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def retrieve_decrypted(db: Session, entity_id: str, field_name: str) -> str | None:
    record = db.query(EncryptedField).filter(
        EncryptedField.entity_id == entity_id,
        EncryptedField.field_name == field_name,
        EncryptedField.deleted_at == None,
    ).first()
    if not record:
        return None
    if record.expires_at and record.expires_at < datetime.now(timezone.utc):
        return None
    return decrypt_sensitive(record.encrypted_value)

def soft_delete(db: Session, entity_id: str, field_name: str) -> bool:
    record = db.query(EncryptedField).filter(
        EncryptedField.entity_id == entity_id,
        EncryptedField.field_name == field_name,
        EncryptedField.deleted_at == None,
    ).first()
    if not record:
        return False
    record.deleted_at = datetime.now(timezone.utc)
    db.commit()
    return True

def rotate_key(db: Session, entity_id: str, field_name: str, new_key_version: int) -> bool:
    record = db.query(EncryptedField).filter(
        EncryptedField.entity_id == entity_id,
        EncryptedField.field_name == field_name,
        EncryptedField.deleted_at == None,
    ).first()
    if not record:
        return False
    plaintext = decrypt_sensitive(record.encrypted_value)
    record.encrypted_value = encrypt_sensitive(plaintext)
    record.key_version = new_key_version
    db.commit()
    return True

def cleanup_expired(db: Session) -> int:
    now = datetime.now(timezone.utc)
    count = db.query(EncryptedField).filter(
        EncryptedField.expires_at != None,
        EncryptedField.expires_at < now,
        EncryptedField.deleted_at == None,
    ).update({"deleted_at": now})
    db.commit()
    return count

def get_encrypted_records_without_sensitive_data(db: Session, entity_id: str) -> list[dict]:
    records = db.query(EncryptedField).filter(EncryptedField.entity_id == entity_id, EncryptedField.deleted_at == None).all()
    return [{"id": r.id, "field_name": r.field_name, "key_version": r.key_version, "has_value": bool(r.encrypted_value)} for r in records]
