from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.models.customer import Customer
from backend.models.transaction import Transaction



class AnalyticsRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_total_customers(self, org_id: int):
        return (
            self.db.query(Customer)
            .filter(
                Customer.org_id == org_id,
                Customer.is_active == True
            )
            .count()
        )

    def get_active_customers(self, org_id: int):
        return (
            self.db.query(Transaction.customer_id)
            .filter(Transaction.org_id == org_id)
            .distinct()
            .count()
        )

    def get_total_transactions(self, org_id: int):
        return (
            self.db.query(Transaction)
            .filter(Transaction.org_id == org_id)
            .count()
        )

    def get_total_revenue(self, org_id: int):
        revenue = (
            self.db.query(func.sum(Transaction.amount))
            .filter(
                Transaction.org_id == org_id
            )
            .scalar()
        )

        return revenue or 0

    def get_average_order_value(self, org_id: int):

        avg = (
            self.db.query(func.avg(Transaction.amount))
            .filter(Transaction.org_id == org_id)
            .scalar()
        )

        return round(avg or 0, 2)

    def get_average_purchase_frequency(self, org_id: int):

        total_transactions = self.get_total_transactions(org_id)

        active_customers = self.get_active_customers(org_id)

        if active_customers == 0:
            return 0

        return round(total_transactions / active_customers, 2)
    
    #revenue by category
    def get_revenue_by_category(self, org_id: int):

        results = (
            self.db.query(
                Transaction.product_category,
                func.sum(Transaction.amount)
            )
            .filter(
                Transaction.org_id == org_id,
                Transaction.status == "Completed"
            )
            .group_by(Transaction.product_category)
            .order_by(func.sum(Transaction.amount).desc())
            .all()
        )

        return [
            {
                "category": row[0],
                "revenue": float(row[1])
            }
            for row in results
        ]
    
    #revenue by payment method
    def get_revenue_by_payment_method(self, org_id: int):

        results = (
            self.db.query(
                Transaction.payment_method,
                func.sum(Transaction.amount)
            )
            .filter(
                Transaction.org_id == org_id,
                Transaction.status == "Completed"
            )
            .group_by(Transaction.payment_method)
            .all()
        )

        return [
            {
                "payment_method": row[0],
                "revenue": float(row[1])
            }
            for row in results
        ]
    
    #monthly revenue
    def get_monthly_revenue(self, org_id: int):

        results = (
            self.db.query(
                func.to_char(Transaction.transaction_date, "YYYY-MM"),
                func.sum(Transaction.amount)
            )
            .filter(
                Transaction.org_id == org_id,
                Transaction.status == "Completed"
            )
            .group_by(
                func.to_char(Transaction.transaction_date, "YYYY-MM")
            )
            .order_by(
                func.to_char(Transaction.transaction_date, "YYYY-MM")
            )
            .all()
        )

        return [
            {
                "period": row[0],
                "revenue": float(row[1])
            }
            for row in results
        ]
    
    def get_customer_growth(self, org_id: int):

        results = (
            self.db.query(
                func.to_char(Customer.created_at, 'YYYY-MM'),
                func.count(Customer.id)
            )
            .filter(
                Customer.org_id == org_id,
                Customer.is_active == True
            )
            .group_by(
                func.to_char(Customer.created_at, 'YYYY-MM')
            )
            .order_by(
                func.to_char(Customer.created_at, 'YYYY-MM')
            )
            .all()
        )

        return [
            {
                "period": row[0],
                "new_customers": row[1]
            }
            for row in results
        ]
    
    def get_average_customer_spend(self, org_id: int):

        revenue = self.get_total_revenue(org_id)

        active_customers = self.get_active_customers(org_id)

        if active_customers == 0:
            return 0

        return round(revenue / active_customers, 2)
    
    def get_repeat_customers(self, org_id: int):
        return(
            self.db.query(Transaction.customer_id)
            .filter(
                Transaction.org_id == org_id,
                Transaction.status == "Completed"
            )
            .group_by(Transaction.customer_id)
            .having(func.count(Transaction.id) >= 2)
            .count()
         )
        
    #One Time Customers
    def get_one_time_customers(self, org_id: int):

        return (
            self.db.query(Transaction.customer_id)
            .filter(
                Transaction.org_id == org_id,
                Transaction.status == "Completed"
            )
            .group_by(Transaction.customer_id)
            .having(func.count(Transaction.id) == 1)
            .count()
        )
    
    #Retention Summary

    def get_retention_summary(self, org_id: int):

        total = self.get_active_customers(org_id)

        repeat = self.get_repeat_customers(org_id)

        one_time = self.get_one_time_customers(org_id)

        retention_rate = 0

        repeat_purchase_rate = 0

        if total > 0:

            retention_rate = round((repeat / total) * 100, 2)

            repeat_purchase_rate = round((repeat / total) * 100, 2)

        return {
            "total_customers": total,
            "repeat_customers": repeat,
            "one_time_customers": one_time,
            "retention_rate": retention_rate,
            "repeat_purchase_rate": repeat_purchase_rate,
        }
    #top customer
    def get_top_customers(self, org_id: int, limit: int = 10):

        results = (
            self.db.query(
                Customer.id,
                Customer.name,
                func.sum(Transaction.amount)
            )
            .join(
                Transaction,
                Customer.id == Transaction.customer_id
            )
            .filter(
                Customer.org_id == org_id,
                Transaction.status == "Completed"
            )
            .group_by(Customer.id, Customer.name)
            .order_by(func.sum(Transaction.amount).desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "customer_id": row[0],
                "customer_name": row[1],
                "total_spent": float(row[2])
            }
            for row in results
        ]
    
    #top products
    def get_top_customers(self, org_id: int, limit: int = 10):

        results = (
            self.db.query(
                Customer.id,
                Customer.name,
                func.sum(Transaction.amount)
            )
            .join(
                Transaction,
                Customer.id == Transaction.customer_id
            )
            .filter(
                Customer.org_id == org_id,
                Transaction.status == "Completed"
            )
            .group_by(Customer.id, Customer.name)
            .order_by(func.sum(Transaction.amount).desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "customer_id": row[0],
                "customer_name": row[1],
                "total_spent": float(row[2])
            }
            for row in results
        ]
    
    #top categories
    def get_top_categories(self, org_id: int, limit: int = 10):

        results = (
            self.db.query(
                Transaction.product_category,
                func.sum(Transaction.amount)
            )
            .filter(
                Transaction.org_id == org_id,
                Transaction.status == "Completed"
            )
            .group_by(Transaction.product_category)
            .order_by(func.sum(Transaction.amount).desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "category": row[0],
                "revenue": float(row[1])
            }
            for row in results
        ]
    
    #get top cities
    def get_top_cities(self, org_id: int, limit: int = 10):

        results = (
            self.db.query(
                Customer.city,
                func.count(Customer.id)
            )
            .filter(
                Customer.org_id == org_id,
                Customer.is_active == True
            )
            .group_by(Customer.city)
            .order_by(func.count(Customer.id).desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "location": row[0],
                "customers": row[1]
            }
            for row in results
        ]
    
    #get top states
    def get_top_states(self, org_id: int, limit: int = 10):

        results = (
            self.db.query(
                Customer.state,
                func.count(Customer.id)
            )
            .filter(
                Customer.org_id == org_id,
                Customer.is_active == True
            )
            .group_by(Customer.state)
            .order_by(func.count(Customer.id).desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "location": row[0],
                "customers": row[1]
            }
            for row in results
        ]
    
    def get_top_products(self, org_id):

        result = (
            self.db.query(
                Transaction.product_name,
                func.sum(Transaction.quantity).label("total_quantity"),
                func.sum(Transaction.amount).label("revenue"),
            )
            .filter(
                Transaction.org_id == org_id,
                Transaction.status == "Completed",
            )
            .group_by(Transaction.product_name)
            .order_by(func.sum(Transaction.quantity).desc())
            .limit(10)
            .all()
        )

        return [
            {
                "product_name": row.product_name,
                "quantity_sold": row.total_quantity,
                "revenue": row.revenue,
            }
            for row in result
        ]