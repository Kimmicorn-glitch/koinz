from pydantic import BaseModel
from datetime import datetime

class StoreEncryptedRequest(BaseModel):
    entity_id: str
    field_name: str
    plaintext: str

class StoreEncryptedResponse(BaseModel):
    id: str
    entity_id: str
    field_name: str
    key_version: int

class RetrieveEncryptedResponse(BaseModel):
    entity_id: str
    field_name: str
    plaintext: str | None

class VaultRecordOut(BaseModel):
    id: str
    field_name: str
    key_version: int
    has_value: bool

class KeyRotationResponse(BaseModel):
    rotated: bool
    entity_id: str
    field_name: str
