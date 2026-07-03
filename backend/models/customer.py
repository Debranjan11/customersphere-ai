from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.database.base import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    org_id = Column(Integer, ForeignKey("organizations.id"))

    customer_code = Column(String, unique=True)

    name = Column(String)

    email = Column(String)

    phone = Column(String)

    city = Column(String)

    organization = relationship(
        "Organization",
        back_populates="customers"
    )

    transactions = relationship(
        "Transaction",
        back_populates="customer"
    )