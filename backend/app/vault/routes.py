from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession
from app.core.security import Roles, require_roles
from app.db.session import get_db
from app.vault.schemas import StoreEncryptedRequest, StoreEncryptedResponse, RetrieveEncryptedResponse, VaultRecordOut, KeyRotationResponse
from app.vault.service import store_encrypted, retrieve_decrypted, soft_delete, rotate_key, get_encrypted_records_without_sensitive_data

router = APIRouter()

@router.post("/store", response_model=StoreEncryptedResponse)
def store(payload: StoreEncryptedRequest, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    r = store_encrypted(db, entity_id=payload.entity_id, field_name=payload.field_name, plaintext=payload.plaintext)
    return StoreEncryptedResponse(id=r.id, entity_id=r.entity_id, field_name=r.field_name, key_version=r.key_version)

@router.get("/retrieve/{entity_id}/{field_name}", response_model=RetrieveEncryptedResponse)
def retrieve(entity_id: str, field_name: str, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    plaintext = retrieve_decrypted(db, entity_id, field_name)
    return RetrieveEncryptedResponse(entity_id=entity_id, field_name=field_name, plaintext=plaintext)

@router.delete("/{entity_id}/{field_name}")
def delete(entity_id: str, field_name: str, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    ok = soft_delete(db, entity_id, field_name)
    return {"deleted": ok}

@router.post("/rotate", response_model=KeyRotationResponse)
def rotate(entity_id: str, field_name: str, new_version: int = 2, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    ok = rotate_key(db, entity_id, field_name, new_version)
    return KeyRotationResponse(rotated=ok, entity_id=entity_id, field_name=field_name)

@router.get("/records/{entity_id}", response_model=list[VaultRecordOut])
def records(entity_id: str, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    return get_encrypted_records_without_sensitive_data(db, entity_id)
