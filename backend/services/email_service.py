"""
Email Service – Sends OTP emails.
Uses a 'fake' adapter by default (prints to console) for local development.
Switch to 'smtp' via EMAIL_BACKEND env var for real email delivery.
"""
import smtplib
from email.mime.text import MIMEText
from config import Config


class FakeEmailAdapter:
    """Prints OTP to console instead of sending a real email."""

    def send(self, to: str, subject: str, body: str):
        print(f"\n{'='*50}")
        print(f"[FAKE EMAIL] to: {to}")
        print(f"   Subject: {subject}")
        print(f"   Body: {body}")
        print(f"{'='*50}\n")
        return True


class SmtpEmailAdapter:
    """Sends email via SMTP."""

    def send(self, to: str, subject: str, body: str):
        msg = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["From"] = Config.SMTP_FROM
        msg["To"] = to
        try:
            with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as server:
                if Config.SMTP_USER:
                    server.starttls()
                    server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"[EmailService] SMTP error: {e}")
            return False


def _get_adapter():
    if Config.EMAIL_BACKEND == "smtp":
        return SmtpEmailAdapter()
    return FakeEmailAdapter()


def send_otp_email(to: str, otp_code: str) -> bool:
    """Send an OTP verification email."""
    subject = "FinSight – Verify Your Email"
    body = f"""
    <h2>Welcome to FinSight!</h2>
    <p>Your verification code is:</p>
    <h1 style="color: #FF9F1C; letter-spacing: 4px;">{otp_code}</h1>
    <p>This code expires in {Config.OTP_EXPIRY_MINUTES} minutes.</p>
    <p style="color: #888;">If you didn't sign up, please ignore this email.</p>
    """
    adapter = _get_adapter()
    return adapter.send(to, subject, body)


def send_login_otp(to: str, otp_code: str, method: str = "email") -> bool:
    """Send/display a login OTP."""
    subject = "FinSight – Login OTP"
    body = f"""
    <h2>Login to FinSight</h2>
    <p>Your one-time login code is:</p>
    <h1 style="color: #2EC4B6; letter-spacing: 4px;">{otp_code}</h1>
    <p>This code expires in {Config.OTP_EXPIRY_MINUTES} minutes.</p>
    <p style="color: #888;">If you didn't request this, please ignore.</p>
    """
    adapter = _get_adapter()
    return adapter.send(to, subject, body)


def send_password_reset_otp(to: str, otp_code: str) -> bool:
    """Send a password reset OTP."""
    subject = "FinSight – Password Reset"
    body = f"""
    <h2>Reset Your Password</h2>
    <p>Your password reset code is:</p>
    <h1 style="color: #E63946; letter-spacing: 4px;">{otp_code}</h1>
    <p>This code expires in {Config.OTP_EXPIRY_MINUTES} minutes.</p>
    <p style="color: #888;">If you didn't request this, please ignore.</p>
    """
    adapter = _get_adapter()
    return adapter.send(to, subject, body)
