from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.models.otp import OTP
from app.utils.otp import generate_otp
from app.utils.email import send_otp_email   # <-- add email sending
from app.schemas.auth import Register, Login, OTPVerify, ResetPassword
from app.core.security import hash_password, verify_password

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================
# REGISTER
# ==========================
@router.post("/register")
def register(data: Register, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="User exists")

    # Create user
    user = User(
        email=data.email,
        username=data.username,
        password_hash=hash_password(data.password),
        is_verified=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate OTP
    otp = generate_otp()
    otp_record = OTP(user_id=user.id, otp=otp, purpose="register")
    db.add(otp_record)
    db.commit()

    # Send OTP via email
    send_otp_email(user.email, otp)

    return {"message": "OTP sent to email"}


# ==========================
# VERIFY OTP
# ==========================
@router.post("/verify-otp")
def verify(data: OTPVerify, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    record = db.query(OTP).filter(
        OTP.user_id == user.id,
        OTP.otp == data.otp,
        OTP.purpose == "register"
    ).first()

    if not record:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    user.is_verified = True
    db.delete(record)
    db.commit()

    return {"message": "Account verified"}


# ==========================
# LOGIN
# ==========================
@router.post("/login")
def login(data: Login, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Account not verified")

    return {"message": "Login success"}


# ==========================
# FORGOT PASSWORD
# ==========================
@router.post("/forgot-password")
def forgot(data: OTPVerify, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp = generate_otp()
    otp_record = OTP(user_id=user.id, otp=otp, purpose="forgot_password")
    db.add(otp_record)
    db.commit()

    # Send OTP via email
    send_otp_email(user.email, otp)

    return {"message": "OTP sent to email"}


# ==========================
# RESET PASSWORD
# ==========================
@router.post("/reset-password")
def reset(data: ResetPassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    record = db.query(OTP).filter(
        OTP.user_id == user.id,
        OTP.otp == data.otp,
        OTP.purpose == "forgot_password"
    ).first()

    if not record:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    user.password_hash = hash_password(data.new_password)
    db.delete(record)
    db.commit()

    return {"message": "Password updated"}
