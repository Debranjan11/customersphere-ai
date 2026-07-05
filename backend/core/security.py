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


def create_access_token(
    *,
    user_id: int,
    org_id: int,
    role: str,
):
    payload = {
        "user_id": user_id,
        "org_id": org_id,
        "role": role,
        "exp": datetime.utcnow()
        + timedelta(
            minutes=settings.security.access_token_expire_minutes
        ),
    }

    return jwt.encode(
        payload,
        settings.security.secret_key,
        algorithm=settings.security.algorithm,
    )


def decode_access_token(token: str):

    try:

        payload = jwt.decode(
            token,
            settings.security.secret_key,
            algorithms=[settings.security.algorithm],
        )
        print("Decoded payload:",payload)
        return payload

    except JWTError as e:
        print("JWT ERROR:", repr(e))
        return None