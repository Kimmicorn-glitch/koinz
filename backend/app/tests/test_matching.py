from app.matching.service import skill_gap, weighted_score


def test_skill_gap() -> None:
    missing = skill_gap(["Electrical", "Safety"], ["electrical"])
    assert missing == ["safety"]


def test_weighted_score_range() -> None:
    score = weighted_score(["a", "b"], ["a"], experience_years=4)
    assert 0.0 <= score <= 1.0
