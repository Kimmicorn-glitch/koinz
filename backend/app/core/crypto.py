"""Field-level encryption for sensitive values."""

from cryptography.fernet import Fernet, InvalidToken

from app.core.config import settings


def _fernet() -> Fernet:
    if not settings.data_encryption_key:
        raise RuntimeError("DATA_ENCRYPTION_KEY is not configured")
    try:
        return Fernet(settings.data_encryption_key.encode("ascii"))
    except (ValueError, TypeError) as exc:
        raise RuntimeError("DATA_ENCRYPTION_KEY must be a valid Fernet key") from exc


def encrypt_sensitive(value: str) -> str:
    if not value:
        return value
    return _fernet().encrypt(value.encode("utf-8")).decode("ascii")


def decrypt_sensitive(value: str) -> str:
    if not value:
        return value
    try:
        return _fernet().decrypt(value.encode("ascii")).decode("utf-8")
    except (InvalidToken, UnicodeError, ValueError) as exc:
        raise RuntimeError("Unable to decrypt sensitive value") from exc
