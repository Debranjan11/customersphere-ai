from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from backend.database.base import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    org_id = Column(
        Integer,
        ForeignKey("organizations.id")
    )

    name = Column(String)

    email = Column(
        String,
        unique=True
    )

    password_hash = Column(String)

    role = Column(String)