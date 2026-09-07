from pydantic import BaseModel, Field


class ProfileCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=7, max_length=32)
    township: str = Field(min_length=2, max_length=120)
    skills: list[str] = Field(default_factory=list)
    resume_obs_key: str | None = None


class ProfileResponse(ProfileCreate):
    id: str
    user_id: str
