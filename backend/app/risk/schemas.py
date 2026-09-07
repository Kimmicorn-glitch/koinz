from pydantic import BaseModel, Field

class RiskEventCreate(BaseModel):
    entity_id: str
    event_type: str
    severity: str = Field(pattern=r"^(low|medium|high|critical)$")
    reason_codes: list[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)

class RiskEventOut(BaseModel):
    id: str
    entity_id: str
    event_type: str
    severity: str
    reason_codes: list[str]
    created_at: str

class RiskScoreOut(BaseModel):
    id: str
    entity_id: str
    score: float
    version: int
    reason_codes: list[str]
    model_version: str
    computed_at: str

class DetectionRuleOut(BaseModel):
    id: str
    name: str
    rule_type: str
    config: dict
    enabled: bool
