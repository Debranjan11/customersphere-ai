from services.api_client import api_client


class TransactionService:

    # ---------------------------------
    # Get All Transactions
    # ---------------------------------

    def get_transactions(
        self,
        token,
        page=1,
        page_size=10,
        keyword=None,
        category=None,
        payment_method=None,
        status=None,
        sort_by="transaction_date",
        sort_order="desc",
    ):

        params = {
            "page": page,
            "page_size": page_size,
            "sort_by": sort_by,
            "sort_order": sort_order,
        }

        if keyword:
            params["keyword"] = keyword

        if category:
            params["category"] = category

        if payment_method:
            params["payment_method"] = payment_method

        if status:
            params["status"] = status

        return api_client.get(
            "/transactions/",
            token=token,
            params=params,
        )

    # ---------------------------------
    # Get Transaction
    # ---------------------------------

    def get_transaction(
        self,
        token,
        transaction_id,
    ):

        return api_client.get(
            f"/transactions/{transaction_id}",
            token=token,
        )

    # ---------------------------------
    # Create Transaction
    # ---------------------------------

    def create_transaction(
        self,
        token,
        transaction,
    ):

        return api_client.post(
            "/transactions/",
            data=transaction,
            token=token,
        )

    # ---------------------------------
    # Update Transaction
    # ---------------------------------

    def update_transaction(
        self,
        token,
        transaction_id,
        transaction,
    ):

        return api_client.put(
            f"/transactions/{transaction_id}",
            data=transaction,
            token=token,
        )

    # ---------------------------------
    # Delete Transaction
    # ---------------------------------

    def delete_transaction(
        self,
        token,
        transaction_id,
    ):

        return api_client.delete(
            f"/transactions/{transaction_id}",
            token=token,
        )

    # ---------------------------------
    # Customer History
    # ---------------------------------

    def customer_transactions(
        self,
        token,
        customer_id,
    ):

        return api_client.get(
            f"/transactions/customer/{customer_id}",
            token=token,
        )


transaction_service = TransactionService()