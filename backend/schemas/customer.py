from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr


# ----------------------------------------
# Base Schema
# ----------------------------------------

class CustomerBase(BaseModel):

    name: str

    email: EmailStr

    phone: Optional[str] = None

    gender: Optional[str] = None

    age: Optional[int] = None

    city: Optional[str] = None

    state: Optional[str] = None

    country: Optional[str] = None

    postal_code: Optional[str] = None


# ----------------------------------------
# Create Customer
# ----------------------------------------

class CustomerCreate(CustomerBase):
    pass


# ----------------------------------------
# Update Customer
# ----------------------------------------

class CustomerUpdate(CustomerBase):
    pass


# ----------------------------------------
# Response Schema
# ----------------------------------------

class CustomerResponse(CustomerBase):

    id: int

    customer_code: str

    org_id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True

class CustomerListResponse(BaseModel):

    total: int

    page: int

    page_size: int

    customers: list[CustomerResponse]