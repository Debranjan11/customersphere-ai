from enum import Enum

from pydantic import BaseModel
from pydantic import EmailStr


# ----------------------------------------
# User Roles
# ----------------------------------------

class UserRole(str, Enum):
    ADMIN = "Admin"
    MANAGER = "Manager"
    ANALYST = "Analyst"


# ----------------------------------------
# Register Request
# ----------------------------------------

class RegisterRequest(BaseModel):

    organization_name: str

    industry: str

    organization_email: EmailStr

    admin_name: str

    admin_email: EmailStr

    password: str


# ----------------------------------------
# Login Request
# ----------------------------------------

class LoginRequest(BaseModel):

    email: EmailStr

    password: str


# ----------------------------------------
# Token Response
# ----------------------------------------

class TokenResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"


# ----------------------------------------
# User Response
# ----------------------------------------

class UserResponse(BaseModel):

    id: int

    name: str

    email: EmailStr

    role: UserRole

    org_id: int

    class Config:
        from_attributes = True