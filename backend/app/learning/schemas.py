from pydantic import BaseModel, Field

class FeedbackCreate(BaseModel):
    decision_id: str
    feedback_type: str = Field(pattern=r"^(true_positive|false_positive|true_negative|false_negative)$")
    notes: str = Field(default="", max_length=500)

class FeedbackOut(BaseModel):
    id: str
    decision_id: str
    feedback_type: str
    analyst_id: str
    notes: str
    created_at: str

class ModelVersionCreate(BaseModel):
    model_name: str
    version: str
    config: dict = Field(default_factory=dict)

class ModelVersionOut(BaseModel):
    id: str
    model_name: str
    version: str
    config: dict
    status: str
    deployed_by: str
    deployed_at: str | None

class ChangeRequestCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    change_type: str
    metadata: dict = Field(default_factory=dict)

class ChangeRequestOut(BaseModel):
    id: str
    title: str
    description: str
    change_type: str
    status: str
    proposed_by: str
    reviewed_by: str | None
    approved_by: str | None
    created_at: str
    updated_at: str

class AdvanceChangeRequest(BaseModel):
    target_status: str
