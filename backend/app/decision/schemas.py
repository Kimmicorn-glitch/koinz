from pydantic import BaseModel, Field

class DecisionCreate(BaseModel):
    entity_id: str
    decision_type: str
    outcome: str = Field(pattern=r"^(approve|deny|human_review)$")
    reason: str = Field(default="", max_length=500)
    policy_ids: list[str] = Field(default_factory=list)
    risk_score_id: str | None = None

class DecisionOut(BaseModel):
    id: str
    entity_id: str
    decision_type: str
    outcome: str
    reason: str
    policy_ids: list[str]
    reviewer_id: str | None
    created_by: str
    created_at: str

class AIRecommendationCreate(BaseModel):
    decision_id: str
    recommendation: str = Field(pattern=r"^(approve|deny|review)$")
    confidence: float = Field(ge=0.0, le=1.0)
    reasons: list[str] = Field(default_factory=list)
    explanation: str = Field(default="", max_length=1000)

class AIRecommendationOut(BaseModel):
    id: str
    decision_id: str
    recommendation: str
    confidence: float
    reasons: list[str]
    model_version: str
    explanation: str

class ReviewRequest(BaseModel):
    outcome: str = Field(pattern=r"^(approve|deny)$")
