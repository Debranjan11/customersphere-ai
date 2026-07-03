from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from backend.core import settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=settings.security.access_token_expire_minutes
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.security.secret_key,
        algorithm=settings.security.algorithm,
    )


def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.security.secret_key,
            algorithms=[settings.security.algorithm],
        )
        return payload

    except JWTError:
        return None