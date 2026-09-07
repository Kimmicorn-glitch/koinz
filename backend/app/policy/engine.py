"""Deterministic policy evaluation with precedence and conflict handling."""
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.policy.models import Policy, PolicyVersion

def create_policy(db: Session, *, name: str, description: str, policy_type: str, conditions: dict, action: str, priority: int = 0, requires_approval: bool = False, created_by: str = "system") -> Policy:
    existing = db.query(Policy).filter(Policy.name == name).first()
    if existing:
        existing.version += 1
        existing.conditions = conditions
        existing.action = action
        existing.priority = priority
        existing.requires_approval = requires_approval
        db.add(PolicyVersion(
            id=str(uuid.uuid4()), policy_id=existing.id, version=existing.version,
            conditions=conditions, action=action, snapshot={"name": name, "type": policy_type, "action": action},
            created_by=created_by,
        ))
        db.commit()
        db.refresh(existing)
        return existing
    policy = Policy(
        id=str(uuid.uuid4()), name=name, description=description, policy_type=policy_type,
        conditions=conditions, action=action, priority=priority, requires_approval=requires_approval,
        created_by=created_by,
    )
    db.add(policy)
    db.add(PolicyVersion(
        id=str(uuid.uuid4()), policy_id=policy.id, version=1,
        conditions=conditions, action=action, snapshot={"name": name, "type": policy_type, "action": action},
        created_by=created_by,
    ))
    db.commit()
    db.refresh(policy)
    return policy

def evaluate_condition(condition: dict, context: dict) -> bool:
    field = condition.get("field")
    op = condition.get("operator")
    value = condition.get("value")
    actual = context.get(field)
    if actual is None:
        return False
    if op == "eq":
        return actual == value
    if op == "gt":
        return float(actual) > float(value)
    if op == "lt":
        return float(actual) < float(value)
    if op == "gte":
        return float(actual) >= float(value)
    if op == "lte":
        return float(actual) <= float(value)
    if op == "in":
        return actual in value
    if op == "contains":
        return value in actual
    return False

def evaluate_policy(db: Session, context: dict) -> dict:
    now = datetime.now(timezone.utc)
    active_policies = db.query(Policy).filter(
        Policy.active == True,
        Policy.effective_from <= now,
    ).order_by(Policy.priority.desc()).all()

    results = []
    for policy in active_policies:
        if policy.effective_to and policy.effective_to < now:
            continue
        conditions_met = all(evaluate_condition(c, context) for c in policy.conditions.get("rules", []))
        results.append({
            "policy_id": policy.id,
            "policy_name": policy.name,
            "action": policy.action,
            "conditions_met": conditions_met,
            "requires_approval": policy.requires_approval,
            "version": policy.version,
        })

    if not results:
        return {"decision": "allow", "matched_policies": [], "conflicts": []}

    approved = [r for r in results if r["conditions_met"] and r["action"] == "allow"]
    denied = [r for r in results if r["conditions_met"] and r["action"] == "deny"]

    if denied:
        return {"decision": "deny", "matched_policies": results, "conflicts": []}
    if approved:
        needs_approval = any(r["requires_approval"] for r in approved)
        return {"decision": "needs_approval" if needs_approval else "allow", "matched_policies": results, "conflicts": []}
    return {"decision": "allow", "matched_policies": results, "conflicts": []}
