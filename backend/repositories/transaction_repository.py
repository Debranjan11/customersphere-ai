from sqlalchemy import (
    asc,
    desc,
    func,
    extract,
)
from sqlalchemy.orm import joinedload

from backend.models.transaction import Transaction
from backend.repositories.base_repository import BaseRepository


class TransactionRepository(BaseRepository):

    def create(self, transaction: Transaction):
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction
    
    def create_many(self, transactions: list[Transaction]):

        self.db.add_all(transactions)

        self.db.commit()

        return transactions

    def get_by_id(self, transaction_id: int, org_id: int):
        return (
            self.db.query(Transaction)
            .options(joinedload(Transaction.customer))
            .filter(
                Transaction.id == transaction_id,
                Transaction.org_id == org_id,
            )
            .first()
        )

    def get_all_by_org(
        self,
        org_id: int,
        page: int = 1,
        page_size: int = 10,
        keyword: str | None = None,
        category: str | None = None,
        payment_method: str | None = None,
        status: str | None = None,
        start_date=None,
        end_date=None,
        sort_by: str = "transaction_date",
        sort_order: str = "desc",
    ):

        query = self.db.query(Transaction).filter(
            Transaction.org_id == org_id
        )

        # Product Search
        if keyword:
            query = query.filter(
                Transaction.product_name.ilike(f"%{keyword}%")
            )

        # Category Filter
        if category:
            query = query.filter(
                Transaction.product_category == category
            )

        # Payment Method
        if payment_method:
            query = query.filter(
                Transaction.payment_method == payment_method
            )

        # Status
        if status:
            query = query.filter(
                Transaction.status == status
            )

        # Date Range
        if start_date:
            query = query.filter(
                Transaction.transaction_date >= start_date
            )

        if end_date:
            query = query.filter(
                Transaction.transaction_date <= end_date
            )

        sort_column = getattr(
            Transaction,
            sort_by,
            Transaction.transaction_date,
        )

        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))

        total = query.count()

        transactions = (
            query.offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "transactions": transactions,
        }
    def update(self, transaction: Transaction):
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def delete(self, transaction: Transaction):
        self.db.delete(transaction)
        self.db.commit()

    def get_by_customer(
        self,
        customer_id: int,
        org_id: int,
    ):
        return (
            self.db.query(Transaction)
            .filter(
                Transaction.customer_id == customer_id,
                Transaction.org_id == org_id,
            )
            .all()
        )

    def get_last_transaction(self, org_id: int):
        return (
            self.db.query(Transaction)
            .filter(
                Transaction.org_id == org_id
            )
            .order_by(Transaction.id.desc())
            .first()
        )
    #total revenue
    def get_total_revenue(self, org_id: int):

        revenue = (
            self.db.query(
                func.sum(Transaction.amount)
            )
            .filter(
                Transaction.org_id == org_id,
                Transaction.status == "Completed",
            )
            .scalar()
        )

        return revenue or 0
    
    #total transactions
    def get_total_transactions(self, org_id: int):

        return (
            self.db.query(Transaction)
            .filter(
                Transaction.org_id == org_id,
                Transaction.status == "Completed",
            )
            .count()
        )
    
    #average order value(AOV)

    def get_average_order_value(self, org_id: int):

        avg = (
            self.db.query(
                func.avg(Transaction.amount)
            )
            .filter(
                Transaction.org_id == org_id,
                Transaction.status == "Completed",
            )
            .scalar()
        )

        return round(avg or 0, 2)
    
    #revenue by category
    def get_revenue_by_category(self, org_id: int):

        rows = (
            self.db.query(
                Transaction.product_category,
                func.sum(Transaction.amount),
            )
            .filter(
                Transaction.org_id == org_id,
                Transaction.status == "Completed",
            )
            .group_by(Transaction.product_category)
            .all()
        )

        return [
            {
                "category": row[0],
                "revenue": float(row[1]),
            }
            for row in rows
        ]
    
    #revenue by payment method
    def get_revenue_by_payment_method(self, org_id: int):

        rows = (
            self.db.query(
                Transaction.payment_method,
                func.sum(Transaction.amount),
            )
            .filter(
                Transaction.org_id == org_id,
                Transaction.status == "Completed",
            )
            .group_by(Transaction.payment_method)
            .all()
        )

        return [
            {
                "payment_method": row[0],
                "revenue": float(row[1]),
            }
            for row in rows
        ]
        
    #monthly revenue
    def get_monthly_revenue(self, org_id: int):

        rows = (
            self.db.query(
                extract("month", Transaction.transaction_date),
                func.sum(Transaction.amount),
            )
            .filter(
                Transaction.org_id == org_id,
                Transaction.status == "Completed",
            )
            .group_by(
                extract("month", Transaction.transaction_date)
            )
            .order_by(
                extract("month", Transaction.transaction_date)
            )
            .all()
        )

        return [
            {
                "month": int(row[0]),
                "revenue": float(row[1]),
            }
            for row in rows
        ]
    
    def get_customer_purchase_frequency(self, org_id: int):

        rows = (
            self.db.query(
                Transaction.customer_id,
                func.count(Transaction.id),
            )
            .filter(
                Transaction.org_id == org_id,
                Transaction.status == "Completed",
            )
            .group_by(Transaction.customer_id)
            .order_by(func.count(Transaction.id).desc())
            .all()
        )

        return [
            {
                "customer_id": row[0],
                "purchase_count": row[1],
            }
            for row in rows
        ]
    
    def get_transaction_count(
        self,
        org_id,
    ):

        return (
            self.db.query(
                func.count(Transaction.id)
            )
            .filter(
                Transaction.org_id == org_id
            )
            .scalar()
        )
    
    def get_all_by_organization(
        self,
        org_id,
    ):

        return (
            self.db.query(Transaction)
            .filter(
                Transaction.org_id == org_id
            )
            .all()
        )
