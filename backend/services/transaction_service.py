from fastapi import HTTPException, status

from backend.models.transaction import Transaction
from backend.repositories.transaction_repository import TransactionRepository
from backend.repositories.customer_repository import CustomerRepository


class TransactionService:

    def __init__(self, db):

        self.repository = TransactionRepository(db)
        self.customer_repository = CustomerRepository(db)

#generate transaction code
    def generate_transaction_code(self, org_id: int):

        last_transaction = self.repository.get_last_transaction(org_id)

        if last_transaction is None:
            number = 1
        else:
            number = (
                int(
                    last_transaction.transaction_code.split("-")[-1]
                ) + 1
            )

        return f"ORG{org_id:03d}-TXN-{number:06d}"
    
#create transaction
    def create_transaction(
        self,
        request,
        org_id,
    ):

        customer = self.customer_repository.get_by_id(
            request.customer_id,
            org_id,
        )

        if customer is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found",
            )

        transaction = Transaction(
            org_id=org_id,
            transaction_code=self.generate_transaction_code(org_id),
            customer_id=request.customer_id,
            product_name=request.product_name,
            product_category=request.product_category,
            quantity=request.quantity,
            amount=request.amount,
            payment_method=request.payment_method,
            status=request.status,
        )

        return self.repository.create(transaction)
    
#get all transaction
    def get_all_transactions(
        self,
        org_id,
        page,
        page_size,
        keyword,
        category,
        payment_method,
        status,
        start_date,
        end_date,
        sort_by,
        sort_order,
    ):

        return self.repository.get_all_by_org(
            org_id=org_id,
            page=page,
            page_size=page_size,
            keyword=keyword,
            category=category,
            payment_method=payment_method,
            status=status,
            start_date=start_date,
            end_date=end_date,
            sort_by=sort_by,
            sort_order=sort_order,
        )
    
#get transaction
    def get_transaction(
        self,
        transaction_id,
        org_id,
    ):

        transaction = self.repository.get_by_id(
            transaction_id,
            org_id,
        )

        if transaction is None:
            raise HTTPException(
                status_code=404,
                detail="Transaction not found",
            )

        return transaction
    
#update transaction
    def update_transaction(
        self,
        transaction_id,
        request,
        org_id,
    ):

        transaction = self.get_transaction(
            transaction_id,
            org_id,
        )

        transaction.product_name = request.product_name
        transaction.product_category = request.product_category
        transaction.quantity = request.quantity
        transaction.amount = request.amount
        transaction.payment_method = request.payment_method
        transaction.status = request.status

        return self.repository.update(transaction)
    
#delete transaction
    def delete_transaction(
        self,
        transaction_id,
        org_id,
    ):

        transaction = self.get_transaction(
            transaction_id,
            org_id,
        )

        self.repository.delete(transaction)

        return {
            "message": "Transaction deleted successfully"
        }
    
#customer transaction history
    def get_customer_transactions(
        self,
        customer_id,
        org_id,
    ):

        return self.repository.get_by_customer(
            customer_id,
            org_id,
        )
    
    def get_dashboard_summary(self, org_id):

        return {

            "total_revenue":
                self.repository.get_total_revenue(org_id),

            "total_transactions":
                self.repository.get_total_transactions(org_id),

            "average_order_value":
                self.repository.get_average_order_value(org_id),

            "revenue_by_category":
                self.repository.get_revenue_by_category(org_id),

            "revenue_by_payment_method":
                self.repository.get_revenue_by_payment_method(org_id),

            "monthly_revenue":
                self.repository.get_monthly_revenue(org_id),

            "purchase_frequency":
                self.repository.get_customer_purchase_frequency(org_id),
        }