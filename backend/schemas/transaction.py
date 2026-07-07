from datetime import datetime

from pydantic import BaseModel, Field

from enum import Enum

from backend.models.transaction import Transaction

# ----------------------------------------
# Enums
# ----------------------------------------

class PaymentMethod(str, Enum):
    CASH = "Cash"
    UPI = "UPI"
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    NET_BANKING = "Net Banking"


class TransactionStatus(str, Enum):
    COMPLETED = "Completed"
    PENDING = "Pending"
    CANCELLED = "Cancelled"
    REFUNDED = "Refunded"
# ----------------------------------------
# Base Schema
# ----------------------------------------

class TransactionBase(BaseModel):

    customer_id: int

    product_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    product_category: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )

    quantity: int = Field(
        ...,
        gt=0,
    )

    amount: float = Field(
        ...,
        gt=0,
    )

    payment_method: PaymentMethod

    status: TransactionStatus = TransactionStatus.COMPLETED


# ----------------------------------------
# Create Transaction
# ----------------------------------------

class TransactionCreate(TransactionBase):
    pass


# ----------------------------------------
# Update Transaction
# ----------------------------------------

class TransactionUpdate(TransactionBase):
    pass


# ----------------------------------------
# Response Schema
# ----------------------------------------

class TransactionResponse(TransactionBase):

    id: int

    org_id: int

    transaction_code: str

    transaction_date: datetime

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True

class TransactionListResponse(BaseModel):

    total: int

    page: int

    page_size: int

    transactions: list[TransactionResponse]