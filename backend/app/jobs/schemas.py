from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    title: str = Field(min_length=3, max_length=180)
    description: str = Field(min_length=10, max_length=2000)
    location: str = Field(min_length=2, max_length=180)
    required_skills: list[str] = Field(default_factory=list)


class JobResponse(JobCreate):
    id: str
    employer_id: str
