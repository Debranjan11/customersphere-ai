from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database.base import Base


class Customer(Base):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    org_id = Column(
        Integer,
        ForeignKey("organizations.id"),
        nullable=False,
    )

    customer_code = Column(
        String,
        unique=True,
        nullable=False,
    )

    name = Column(
        String,
        nullable=False,
    )

    email = Column(
        String,
        nullable=False,
    )

    phone = Column(String)

    gender = Column(String)

    age = Column(Integer)

    city = Column(String)

    state = Column(String)

    country = Column(String)

    postal_code = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    is_active = Column(
        Boolean,
        default=True,
    )

    organization = relationship(
        "Organization",
        back_populates="customers",
    )

    transactions = relationship(
        "Transaction",
        back_populates="customer",
    )