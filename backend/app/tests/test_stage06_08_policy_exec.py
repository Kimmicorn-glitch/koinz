from app.policy.engine import evaluate_condition, evaluate_policy
from app.policy.models import Policy


def test_evaluate_condition_eq() -> None:
    condition = {"field": "amount_cents", "operator": "gt", "value": 1000}
    assert evaluate_condition(condition, {"amount_cents": 2000}) is True
    assert evaluate_condition(condition, {"amount_cents": 500}) is False


def test_evaluate_condition_in() -> None:
    condition = {"field": "currency", "operator": "in", "value": ["ZAR", "USD"]}
    assert evaluate_condition(condition, {"currency": "ZAR"}) is True
    assert evaluate_condition(condition, {"currency": "EUR"}) is False


def test_evaluate_condition_missing_field_false() -> None:
    condition = {"field": "unknown_field", "operator": "eq", "value": 10}
    assert evaluate_condition(condition, {"amount": 10}) is False


def test_evaluate_policy_no_policies_allows() -> None:
    from unittest.mock import MagicMock
    db = MagicMock()
    db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
    result = evaluate_policy(db, {"amount_cents": 100})
    assert result["decision"] == "allow"


def test_state_machine_transitions() -> None:
    from app.execution.state_machine import can_transition, get_valid_transitions, is_terminal
    assert can_transition("simulated", "pending") is True
    assert can_transition("pending", "settled") is False  # can't skip submitted
    assert can_transition("settled", "pending") is False  # terminal
    assert is_terminal("settled") is True
    assert is_terminal("submitted") is False
    assert "submitted" in get_valid_transitions("pending")
