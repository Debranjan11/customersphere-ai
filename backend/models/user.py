from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    org_id = Column(Integer, ForeignKey("organizations.id"))

    name = Column(String)

    email = Column(String, unique=True)

    password_hash = Column(String)

    role = Column(String)

    organization = relationship("Organization", back_populates="users")