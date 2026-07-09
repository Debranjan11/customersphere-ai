from services.api_client import api_client


class CustomerService:

    # ---------------------------------
    # Get All Customers
    # ---------------------------------
    def get_customers(
        self,
        token,
        page=1,
        page_size=10,
        keyword=None,
        city=None,
        state=None,
        is_active=True,
        sort_by="created_at",
        sort_order="desc",
    ):

        params = {
            "page": page,
            "page_size": page_size,
            "is_active": is_active,
            "sort_by": sort_by,
            "sort_order": sort_order,
        }

        if keyword:
            params["keyword"] = keyword

        if city:
            params["city"] = city

        if state:
            params["state"] = state

        return api_client.get(
            "/customers/",
            token=token,
            params=params,
        )

    # ---------------------------------
    # Get Customer By ID
    # ---------------------------------
    def get_customer(
        self,
        token,
        customer_id,
    ):

        return api_client.get(
            f"/customers/{customer_id}",
            token=token,
        )

    # ---------------------------------
    # Create Customer
    # ---------------------------------
    def create_customer(
        self,
        token,
        customer_data,
    ):

        return api_client.post(
            "/customers/",
            data=customer_data,
            token=token,
        )

    # ---------------------------------
    # Update Customer
    # ---------------------------------
    def update_customer(
        self,
        token,
        customer_id,
        customer_data,
    ):

        return api_client.put(
            f"/customers/{customer_id}",
            data=customer_data,
            token=token,
        )

    # ---------------------------------
    # Delete Customer
    # ---------------------------------
    def delete_customer(
        self,
        token,
        customer_id,
    ):

        return api_client.delete(
            f"/customers/{customer_id}",
            token=token,
        )

    # ---------------------------------
    # Search Customers
    # ---------------------------------
    def search_customers(
        self,
        token,
        keyword,
    ):

        return api_client.get(
            "/customers/search/",
            token=token,
            params={
                "keyword": keyword,
            },
        )
        # ---------------------------------
    # Customer Dropdown
    # ---------------------------------

    def get_customer_dropdown(
        self,
        token,
    ):

        response = self.get_customers(
            token=token,
            page=1,
            page_size=1000,
        )

        if response.status_code != 200:

            return []

        data = response.json()

        customers = data.get(
            "customers",
            []
        )

        return [
            {
                "id": customer["id"],
                "label": (
                    f"{customer['customer_code']} - "
                    f"{customer['name']}"
                ),
            }
            for customer in customers
        ]

customer_service = CustomerService()