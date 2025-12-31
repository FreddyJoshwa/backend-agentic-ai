from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    username = Column(String(50), unique=True)
    password_hash = Column(String(255))
    is_verified = Column(Boolean, default=False)
