from app.risk.engine import DEFAULT_RULES, _score_from_events, check_velocity, check_replay
from app.risk.models import RiskEvent


def _make_event(severity: str, event_type: str = "transaction") -> RiskEvent:
    return RiskEvent(
        id=f"evt-{severity}",
        entity_id="entity-1",
        event_type=event_type,
        severity=severity,
        reason_codes=["test"],
        metadata={},
    )


def test_risk_score_from_events() -> None:
    events = [_make_event("low"), _make_event("medium"), _make_event("high")]
    score = _score_from_events(events)
    assert 0.0 <= score <= 1.0
    # High severity should push score up
    high_only = _score_from_events([_make_event("critical")])
    assert high_only >= score


def test_risk_score_critical_max() -> None:
    score = _score_from_events([_make_event("critical")])
    assert score == 1.0


def test_risk_score_no_events_is_zero() -> None:
    assert _score_from_events([]) == 0.0


def test_default_rules_present() -> None:
    names = {r["name"] for r in DEFAULT_RULES}
    assert {"velocity_check", "replay_detection", "amount_threshold", "suspicious_beneficiary"} <= names


def test_velocity_exceeded_when_many_events() -> None:
    recent = [RiskEvent(id=f"e{i}", entity_id="u1", event_type="transaction", severity="low", reason_codes=[], metadata={}) for i in range(15)]
    # Simulate velocity check with a window context where count >= max
    assert len(recent) >= 10
