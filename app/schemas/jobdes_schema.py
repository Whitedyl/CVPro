from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class JobDesBase(BaseModel):
    title: str
    required_skills: List[str]
    experience: int
    domain: str
    description_text: str
    feedback: Optional[str] = None

class JobDesResponse(JobDesBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True