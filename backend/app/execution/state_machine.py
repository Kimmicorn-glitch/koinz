"""Execution state machine with valid transitions."""

VALID_TRANSITIONS = {
    "simulated": ["pending"],
    "pending": ["submitted"],
    "submitted": ["acknowledged", "failed", "unknown"],
    "acknowledged": ["settled", "failed", "reconciliation_required"],
    "failed": ["pending"],  # retry
    "unknown": ["pending", "reconciliation_required"],
    "reconciliation_required": ["settled", "failed"],
    "settled": [],  # terminal
}

def can_transition(current: str, target: str) -> bool:
    return target in VALID_TRANSITIONS.get(current, [])

def get_valid_transitions(current: str) -> list[str]:
    return VALID_TRANSITIONS.get(current, [])

def is_terminal(status: str) -> bool:
    return status == "settled"
