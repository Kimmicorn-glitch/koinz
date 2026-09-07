from pydantic import BaseModel, Field
from datetime import datetime

class PolicyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=500)
    policy_type: str = Field(min_length=1, max_length=64)
    conditions: dict
    action: str = Field(pattern=r"^(allow|deny|needs_approval)$")
    priority: int = Field(default=0)
    requires_approval: bool = Field(default=False)

class PolicyOut(BaseModel):
    id: str
    name: str
    policy_type: str
    action: str
    priority: int
    version: int
    active: bool
    requires_approval: bool

class PolicyEvaluateRequest(BaseModel):
    context: dict

class PolicyEvaluateResponse(BaseModel):
    decision: str
    matched_policies: list[dict]
    conflicts: list[dict]
