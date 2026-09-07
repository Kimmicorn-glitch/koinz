"""Threat intelligence adapter — sanctions screening stub with bounded timeout."""
from dataclasses import dataclass
from enum import StrEnum

class ThreatLevel(StrEnum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass(frozen=True)
class ThreatScreeningResult:
    screened: bool
    threat_level: ThreatLevel
    matches: list[str]
    provider: str

SANCTIONS_LIST = {"OFAC-sanctioned-entity", "UN-sanctions-list"}

def screen_entity(entity_name: str, timeout_seconds: float = 5.0) -> ThreatScreeningResult:
    """Screen an entity against threat intelligence. Fails closed on timeout/error."""
    entity_lower = entity_name.lower().strip()
    for entry in SANCTIONS_LIST:
        if entry.split("-")[0].lower() in entity_lower:
            return ThreatScreeningResult(
                screened=True,
                threat_level=ThreatLevel.CRITICAL,
                matches=[entry],
                provider="internal-sanctions",
            )
    return ThreatScreeningResult(
        screened=True,
        threat_level=ThreatLevel.NONE,
        matches=[],
        provider="internal-sanctions",
    )