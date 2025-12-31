from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True)
    username = Column(String(50), unique=True)
    password = Column(String(255))
    is_verified = Column(Boolean, default=False)
