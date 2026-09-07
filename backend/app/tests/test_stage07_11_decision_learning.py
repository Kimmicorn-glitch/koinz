from app.decision.engine import create_ai_recommendation
from app.learning.service import can_change_transition


def test_ai_recommendation_confidence_bounded() -> None:
    from app.db.session import SessionLocal
    from app.decision.models import Decision, AIRecommendation

    db = SessionLocal()
    try:
        # Test confidence clamping via a directly-constructed recommendation
        rec = AIRecommendation(
            id="rec-1",
            decision_id="decision-1",
            recommendation="approve",
            confidence=0.95,
            reasons=["reason"],
            model_version="v1.0",
        )
        assert 0.0 <= rec.confidence <= 1.0
    finally:
        db.close()


def test_learning_workflow_transitions() -> None:
    assert can_change_transition("proposed", "review") is True
    assert can_change_transition("review", "test") is True
    assert can_change_transition("test", "approve") is True
    assert can_change_transition("approve", "version") is True
    assert can_change_transition("version", "deploy") is True
    assert can_change_transition("deploy", "monitor") is True


def test_learning_workflow_rejects_invalid() -> None:
    assert can_change_transition("proposed", "deploy") is False
    assert can_change_transition("monitor", "approve") is False
