from sqlalchemy import Column, Integer, String, Text, ARRAY, DateTime
from app.database import Base
import datetime

class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    required_skills = Column(ARRAY(String))
    experience = Column(Integer)
    domain = Column(String, index=True)
    description_text = Column(Text)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))