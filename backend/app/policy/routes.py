from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession
from app.core.security import Roles, require_roles
from app.db.session import get_db
from app.policy.schemas import PolicyCreate, PolicyOut, PolicyEvaluateRequest, PolicyEvaluateResponse
from app.policy.engine import create_policy, evaluate_policy
from app.policy.models import Policy

router = APIRouter()

@router.post("/", response_model=PolicyOut)
def create(payload: PolicyCreate, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    p = create_policy(db, name=payload.name, description=payload.description, policy_type=payload.policy_type, conditions=payload.conditions, action=payload.action, priority=payload.priority, requires_approval=payload.requires_approval, created_by=user["id"])
    return PolicyOut(id=p.id, name=p.name, policy_type=p.policy_type, action=p.action, priority=p.priority, version=p.version, active=p.active, requires_approval=p.requires_approval)

@router.get("/", response_model=list[PolicyOut])
def list_policies(user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    policies = db.query(Policy).all()
    return [PolicyOut(id=p.id, name=p.name, policy_type=p.policy_type, action=p.action, priority=p.priority, version=p.version, active=p.active, requires_approval=p.requires_approval) for p in policies]

@router.post("/evaluate", response_model=PolicyEvaluateResponse)
def evaluate(payload: PolicyEvaluateRequest, user: dict = Depends(require_roles({Roles.ADMIN})), db: DBSession = Depends(get_db)):
    result = evaluate_policy(db, payload.context)
    return PolicyEvaluateResponse(**result)
