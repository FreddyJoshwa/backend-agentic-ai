import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_FROM = "otpsenderforproject@gmail.com"
EMAIL_PASSWORD = "frxkptcaekxnsdxc"

def send_otp_email(to_email: str, otp: str):
    msg = MIMEText(f"Your OTP is: {otp}")
    msg["Subject"] = "CareerMate OTP Verification"
    msg["From"] = EMAIL_FROM
    msg["To"] = to_email

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_FROM, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()
