from sqlalchemy import Column, Integer, String, Text, ARRAY
from app.database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    skills = Column(ARRAY(String))
    experience = Column(Integer)
    domain = Column(String, index=True)
    cv_text = Column(Text)
    feedback = Column(Text)
