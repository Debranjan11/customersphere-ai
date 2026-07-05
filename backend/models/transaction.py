from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from backend.database.base import Base


class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    org_id = Column(
        Integer,
        ForeignKey("organizations.id"),
        nullable=False,
    )

    transaction_code = Column(
        String,
        nullable=False,
        unique=True,
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False,
    )

    product_name = Column(
        String,
        nullable=False,
    )

    product_category = Column(
        String,
        nullable=False,
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=1,
    )

    amount = Column(
        Float,
        nullable=False,
    )

    payment_method = Column(
        String,
        nullable=False,
    )

    status = Column(
        String,
        default="Completed",
    )

    transaction_date = Column(
        DateTime,
        default=datetime.utcnow,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    organization = relationship(
        "Organization",
        back_populates="transactions",
    )

    customer = relationship(
        "Customer",
        back_populates="transactions",
    )