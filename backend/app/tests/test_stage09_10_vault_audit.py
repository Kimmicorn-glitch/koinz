from unittest.mock import MagicMock

from app.vault.service import get_encrypted_records_without_sensitive_data


def test_vault_records_do_not_expose_sensitive_data() -> None:
    db = MagicMock()
    # Build a fake record with encrypted value - should expose only metadata
    class FakeRecord:
        id = "rec-1"
        field_name = "account_number"
        key_version = 1
        encrypted_value = "gAAAAABencrypted-blob"

    db.query.return_value.filter.return_value.all.return_value = [FakeRecord()]
    records = get_encrypted_records_without_sensitive_data(db, "entity-1")
    assert records[0]["has_value"] is True
    assert "encrypted_value" not in records[0]
    assert "plaintext" not in records[0]
    assert records[0]["field_name"] == "account_number"


def test_audit_hash_chain_verification() -> None:
    from app.audit.service import _compute_hash
    first_hash = _compute_hash("corr-1", "transaction", "entity-1", {"amount": 100}, "0" * 64, 1)
    second_hash = _compute_hash("corr-1", "transaction", "entity-1", {"amount": 100}, first_hash, 2)
    third_hash = _compute_hash("corr-1", "transaction", "entity-1", {"amount": 100}, second_hash, 3)

    assert first_hash != second_hash != third_hash
    assert len(first_hash) == 64


def test_audit_hash_contains_previous_chain() -> None:
    from app.audit.service import _compute_hash
    h1 = _compute_hash("c1", "t", "e", {"a": 1}, "0" * 64, 1)
    h2 = _compute_hash("c1", "t", "e", {"a": 1}, h1, 2)
    assert h2 != h1
    assert len(h2) == 64
