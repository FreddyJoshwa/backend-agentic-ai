from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.schemas.auth import *
from app.core.security import *

router = APIRouter(prefix="/auth")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(data: Register, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(400, "Username exists")

    user = User(
        email=data.email,
        username=data.username,
        password=hash_password(data.password),
        is_verified=False
    )
    db.add(user)
    db.commit()
    generate_otp(data.username)
    return {"message": "OTP sent to registered email"}

@router.post("/verify-otp")
def verify(data: OTPVerify, db: Session = Depends(get_db)):
    if not verify_otp(data.username, data.otp):
        raise HTTPException(400, "Invalid OTP")

    user = db.query(User).filter(User.username == data.username).first()
    user.is_verified = True
    db.commit()
    return {"message": "Account verified"}

@router.post("/login")
def login(data: Login, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(400, "Invalid credentials")

    if not user.is_verified:
        raise HTTPException(400, "Verify OTP first")

    return {"message": "Login successful"}

@router.post("/forgot-password")
def forgot(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user:
        generate_otp(username)
    return {"message": "If account exists, OTP sent"}

@router.post("/reset-password")
def reset(data: ResetPassword, db: Session = Depends(get_db)):
    if not verify_otp(data.username, data.otp):
        raise HTTPException(400, "Invalid OTP")

    user = db.query(User).filter(User.username == data.username).first()
    user.password = hash_password(data.new_password)
    db.commit()
    return {"message": "Password reset successful"}
