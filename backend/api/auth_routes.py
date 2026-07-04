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
from backend.dependencies import (
    get_current_user,
    require_admin,
    require_manager,
    require_analyst,
)

from backend.services.auth_service import AuthService

#protected routes
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from backend.core.security import decode_access_token

security = HTTPBearer()

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

@router.get("/me")
def get_me(
    current_user=Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "organization_id": current_user.org_id,
    }

@router.get("/admin")
def admin_dashboard(
    current_user=Depends(require_admin),
):
    return {
        "message": "Welcome Admin",
        "user": current_user.name,
    }

@router.get("/manager")
def manager_dashboard(
    current_user=Depends(require_manager),
):
    return {
        "message": "Manager Dashboard",
        "user": current_user.name,
    }

@router.get("/analytics")
def analytics_dashboard(
    current_user=Depends(require_analyst),
):
    return {
        "message": "Analytics Dashboard",
        "user": current_user.name,
    }