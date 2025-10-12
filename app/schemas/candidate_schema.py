from pydantic import BaseModel, EmailStr 
from typing import Optional, List
from datetime import datetime

class CandidateBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None  # Make email optional
    skills: List[str]
    experience: int
    domain: Optional[str] = None  # Make domain optional
    cv_text: str
    feedback: Optional[str] = None
    phone: Optional[str] = None
    education: Optional[List[str]] = None
    linkedin_url: Optional[str] = None
    preferred_location: Optional[str] = None
    cv_file_path: Optional[str] = None
    is_active: bool = True

class CandidateResponse(CandidateBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True