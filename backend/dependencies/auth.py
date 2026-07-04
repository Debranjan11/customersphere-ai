from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from backend.database.session import get_db

from backend.repositories.auth_repository import AuthRepository

from backend.core.security import decode_access_token

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):

    token = credentials.credentials

    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    repository = AuthRepository(db)

    user = repository.get_user_by_id(
        payload["user_id"]
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user

def get_current_org(
    current_user=Depends(get_current_user),
):

    return current_user.org_id

def require_admin(
    current_user=Depends(get_current_user),
):

    if current_user.role != "Admin":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return current_user

def require_manager(
    current_user=Depends(get_current_user),
):

    if current_user.role not in [
        "Admin",
        "Manager",
    ]:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager access required",
        )

    return current_user

def require_analyst(
    current_user=Depends(get_current_user),
):

    return current_user