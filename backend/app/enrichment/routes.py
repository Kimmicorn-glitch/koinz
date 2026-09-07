from fastapi import APIRouter
from pydantic import BaseModel
from app.enrichment.service import enrich_transaction

router = APIRouter()

class EnrichRequest(BaseModel):
    amount: float
    currency: str
    holder_name: str
    bank_name: str | None = None

class EnrichResponse(BaseModel):
    normalized: bool
    currency_data: dict
    bank_data: dict | None
    threat_level: str
    threat_matches: list[str]

@router.post("/enrich", response_model=EnrichResponse)
def enrich(payload: EnrichRequest):
    result = enrich_transaction(payload.amount, payload.currency, payload.holder_name, payload.bank_name)
    return EnrichResponse(
        normalized=result.normalized,
        currency_data=result.currency_data,
        bank_data=result.bank_data,
        threat_level=result.threat_level.value,
        threat_matches=result.threat_matches,
    )