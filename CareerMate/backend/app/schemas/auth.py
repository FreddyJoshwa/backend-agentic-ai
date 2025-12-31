from pydantic import BaseModel

class Register(BaseModel):
    email: str
    username: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class OTPVerify(BaseModel):
    username: str
    otp: str

class ResetPassword(BaseModel):
    username: str
    otp: str
    new_password: str
