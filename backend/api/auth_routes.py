from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.database.session import get_db

from backend.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
)

from backend.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    return service.register(request)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):

    service = AuthService(db)

    token = service.login(request)

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    return {
        "access_token": token,
        "token_type": "bearer",
    }

#protected routes
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from backend.core.security import verify_token

security = HTTPBearer()


@router.get("/me")
def me(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
):

    payload = verify_token(
        credentials.credentials
    )

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token",
        )

    return payload