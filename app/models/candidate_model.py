from sqlalchemy import Column, Integer, String, Text, ARRAY, DateTime, Boolean
from app.database import Base
import datetime

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, nullable=True)  # Add this
    skills = Column(ARRAY(String))
    experience = Column(Integer)
    domain = Column(String, index=True, nullable=True)
    cv_text = Column(Text)
    feedback = Column(Text, nullable=True)
    education = Column(ARRAY(String), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    is_active = Column(Boolean, default=True)
    cv_file_path = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    preferred_location = Column(String, nullable=True)

    def __repr__(self):
        return f"<Candidate(id={self.id}, name={self.name}, email={self.email})>"