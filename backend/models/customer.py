from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from backend.database.base import Base

class Customer(Base):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)

    org_id = Column(
        Integer,
        ForeignKey("organizations.id")
    )

    name = Column(String)

    email = Column(String)

    phone = Column(String)

    city = Column(String)