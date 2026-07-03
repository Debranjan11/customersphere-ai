from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import ForeignKey

from backend.database.base import Base

class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)

    org_id = Column(
        Integer,
        ForeignKey("organizations.id")
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id")
    )

    amount = Column(Float)