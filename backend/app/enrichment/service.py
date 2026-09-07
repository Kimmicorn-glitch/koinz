"""Enrichment service combining reference data and threat screening."""
from app.enrichment.reference_data import lookup_currency, lookup_bank, normalize_amount
from app.enrichment.threat_intel import screen_entity, ThreatLevel
from dataclasses import dataclass

@dataclass(frozen=True)
class EnrichedTransaction:
    normalized: bool
    currency_data: dict
    bank_data: dict | None
    threat_level: ThreatLevel
    threat_matches: list[str]

def enrich_transaction(amount: float, currency: str, holder_name: str, bank_name: str | None = None) -> EnrichedTransaction:
    currency_data = lookup_currency(currency).data
    bank_data = lookup_bank(bank_name).data if bank_name else None
    threat = screen_entity(holder_name)
    normalized_amount = normalize_amount(amount, currency)
    return EnrichedTransaction(
        normalized=normalized_amount.get("normalized", False),
        currency_data=currency_data,
        bank_data=bank_data,
        threat_level=threat.threat_level,
        threat_matches=threat.matches,
    )