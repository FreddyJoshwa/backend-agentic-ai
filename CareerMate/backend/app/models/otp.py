from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class OTP(Base):
    __tablename__ = "otp_verification"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    otp = Column(String(6))
    purpose = Column(String(30))
