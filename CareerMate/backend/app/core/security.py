from passlib.context import CryptContext
import random, time

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
otp_store = {}

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

def generate_otp(username):
    otp = str(random.randint(100000, 999999))
    otp_store[username] = {
        "otp": otp,
        "expires": time.time() + 300
    }
    print("OTP:", otp)  # hackathon demo
    return otp

def verify_otp(username, otp):
    data = otp_store.get(username)
    if not data or time.time() > data["expires"]:
        return False
    return data["otp"] == otp
