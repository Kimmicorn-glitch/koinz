"""Field-level encryption for sensitive values.

In non-production environments a missing or invalid ``DATA_ENCRYPTION_KEY``
falls back to an ephemeral key generated for this process (encrypted values
do not survive restarts). Production always requires an explicit, valid key.
"""

from cryptography.fernet import Fernet, InvalidToken

from app.core.config import settings

_DEV_KEY: str | None = None


def _is_production() -> bool:
    return settings.environment.lower() in {"production", "prod"}


def _dev_fernet() -> Fernet:
    global _DEV_KEY
    if _DEV_KEY is None:
        _DEV_KEY = Fernet.generate_key().decode("ascii")
    return Fernet(_DEV_KEY.encode("ascii"))


def _fernet() -> Fernet:
    key = settings.data_encryption_key
    if not key:
        if _is_production():
            raise RuntimeError("DATA_ENCRYPTION_KEY is not configured")
        return _dev_fernet()
    try:
        return Fernet(key.encode("ascii"))
    except (ValueError, TypeError):
        if _is_production():
            raise RuntimeError("DATA_ENCRYPTION_KEY must be a valid Fernet key")
        return _dev_fernet()


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