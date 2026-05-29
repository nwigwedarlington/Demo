from datetime import UTC, datetime, timedelta

from jose import jwt

from app.core.config import get_settings


def create_access_token(subject: str, minutes: int = 60) -> str:
    settings = get_settings()
    expires = datetime.now(UTC) + timedelta(minutes=minutes)
    return jwt.encode({"sub": subject, "exp": expires}, settings.jwt_secret, algorithm="HS256")


def verify_access_token(token: str) -> dict:
    settings = get_settings()
    return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
