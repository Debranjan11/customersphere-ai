from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.database.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    org_id = Column(Integer, ForeignKey("organizations.id"))

    customer_id = Column(Integer, ForeignKey("customers.id"))

    amount = Column(Float)

    payment_method = Column(String)

    organization = relationship(
        "Organization",
        back_populates="transactions"
    )

    customer = relationship(
        "Customer",
        back_populates="transactions"
    )