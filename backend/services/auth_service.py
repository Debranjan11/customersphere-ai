from backend.models.organization import Organization
from backend.models.user import User

from backend.repositories.auth_repository import AuthRepository

from backend.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

from backend.schemas.auth import UserRole


class AuthService:

    def __init__(self, db):
        self.repository = AuthRepository(db)

    def register(self, request):

        organization = Organization(
            name=request.organization_name,
            industry=request.industry,
            email=request.organization_email,
        )

        organization = self.repository.create_organization(
            organization
        )
       
        user = User(
            org_id=organization.id,
            name=request.admin_name,
            email=request.admin_email,
            password_hash=hash_password(
                request.password
            ),
            role=UserRole.ADMIN.value,
        )

        self.repository.create_user(user)

        return {"message": "Organization Registered Successfully"}

    def login(self, request):

        user = self.repository.get_user_by_email(
            request.email
        )

        if not user:
            return None

        if not verify_password(
            request.password,
            user.password_hash,
        ):
            return None

        token = create_access_token(
            {
                "user_id": user.id,
                "org_id": user.org_id,
                "role": user.role,
            }
        )

        return token