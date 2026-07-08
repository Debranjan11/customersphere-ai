from sqlalchemy.orm import Session

from backend.models.customer import Customer
from backend.models.transaction import Transaction


class SegmentationRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_rfm_data(self, org_id: int):

        return (
            self.db.query(
                Customer.id.label("customer_id"),
                Customer.name.label("customer_name"),
                Transaction.transaction_date,
                Transaction.amount,
            )
            .join(
                Transaction,
                Customer.id == Transaction.customer_id
            )
            .filter(
                Customer.org_id == org_id,
                Transaction.org_id == org_id,
                Customer.is_active == True,
                Transaction.status == "Completed",
            )
            .all()
        )