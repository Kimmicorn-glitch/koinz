"""Reference data adapter for currency codes, bank BIN lookups, and static data."""
from dataclasses import dataclass

CURRENCY_CODES = {"ZAR", "USD", "EUR", "GBP", "NGN", "KES", "GHS", "BTC"}
BANK_NAMES = {"FNB", "ABSA", "Standard Bank", "Nedbank", "Capitec", "Investec", "Discovery"}

@dataclass(frozen=True)
class ReferenceDataResult:
    found: bool
    data: dict

def lookup_currency(code: str) -> ReferenceDataResult:
    code = code.upper()
    if code in CURRENCY_CODES:
        return ReferenceDataResult(found=True, data={"code": code, "type": "fiat" if code != "BTC" else "crypto"})
    return ReferenceDataResult(found=False, data={"error": f"Unknown currency: {code}"})

def lookup_bank(bank_name: str) -> ReferenceDataResult:
    for bank in BANK_NAMES:
        if bank.lower() == bank_name.lower():
            return ReferenceDataResult(found=True, data={"name": bank, "country": "ZA"})
    return ReferenceDataResult(found=False, data={"error": f"Unknown bank: {bank_name}"})

def normalize_amount(amount: float, currency: str) -> dict:
    currency = currency.upper()
    if currency == "ZAR":
        return {"amount_cents": int(round(amount * 100)), "currency": "ZAR", "normalized": True}
    return {"amount_raw": amount, "currency": currency, "normalized": False}