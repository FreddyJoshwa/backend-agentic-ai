from sqlalchemy import Column, Integer, String, ForeignKey, Text  # <-- add Text
from app.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    resume_file = Column(String(255))
    goals = Column(String(500))
    skills = Column(String(500))
    missing_skills = Column(Text)   # <-- now no error
