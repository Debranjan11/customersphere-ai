from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from backend.database.base import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    industry = Column(String)

    email = Column(String, unique=True)

    users = relationship("User", back_populates="organization")

    customers = relationship("Customer", back_populates="organization")

    transactions = relationship("Transaction", back_populates="organization")