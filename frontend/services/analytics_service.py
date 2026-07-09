from services.api_client import api_client


class AnalyticsService:

    # ----------------------------------
    # Dashboard
    # ----------------------------------

    def get_dashboard(
        self,
        token,
    ):

        return api_client.get(
            "/analytics/dashboard",
            token=token,
        )

    def get_dashboard_summary(
        self,
        token,
    ):

        return api_client.get(
            "/analytics/dashboard-summary",
            token=token,
        )

    # ----------------------------------
    # Revenue Analytics
    # ----------------------------------

    def get_revenue_by_category(
        self,
        token,
    ):

        return api_client.get(
            "/analytics/revenue/category",
            token=token,
        )

    def get_revenue_by_payment_method(
        self,
        token,
    ):

        return api_client.get(
            "/analytics/revenue/payment-method",
            token=token,
        )

    def get_monthly_revenue(
        self,
        token,
    ):

        return api_client.get(
            "/analytics/revenue/monthly",
            token=token,
        )

    # ----------------------------------
    # Customer Analytics
    # ----------------------------------

    def get_customer_growth(
        self,
        token,
    ):

        return api_client.get(
            "/analytics/customers/growth",
            token=token,
        )

    def get_average_customer_spend(
        self,
        token,
    ):

        return api_client.get(
            "/analytics/customers/average-spend",
            token=token,
        )

    def get_purchase_frequency(
        self,
        token,
    ):

        return api_client.get(
            "/analytics/customers/purchase-frequency",
            token=token,
        )

    def get_retention(
        self,
        token,
    ):

        return api_client.get(
            "/analytics/customers/retention",
            token=token,
        )

    # ----------------------------------
    # Business Insights
    # ----------------------------------

    def get_top_customers(
        self,
        token,
    ):

        return api_client.get(
            "/analytics/insights/top-customers",
            token=token,
        )

    def get_top_products(
        self,
        token,
    ):

        return api_client.get(
            "/analytics/insights/top-products",
            token=token,
        )

    def get_top_categories(
        self,
        token,
    ):

        return api_client.get(
            "/analytics/insights/top-categories",
            token=token,
        )

    def get_top_cities(
        self,
        token,
    ):

        return api_client.get(
            "/analytics/insights/top-cities",
            token=token,
        )

    def get_top_states(
        self,
        token,
    ):

        return api_client.get(
            "/analytics/insights/top-states",
            token=token,
        )


analytics_service = AnalyticsService()