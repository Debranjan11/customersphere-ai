from backend.repositories.analytics_repository import AnalyticsRepository

class AnalyticsService:

    def __init__(self, db):
        self.repo = AnalyticsRepository(db)

    def get_dashboard_summary(self, org_id: int):

        return {
            "total_customers":
                self.repo.get_total_customers(org_id),

            "active_customers":
                self.repo.get_active_customers(org_id),

            "total_transactions":
                self.repo.get_total_transactions(org_id),

            "total_revenue":
                self.repo.get_total_revenue(org_id),

            "average_order_value":
                self.repo.get_average_order_value(org_id),

            "average_purchase_frequency":
                self.repo.get_average_purchase_frequency(org_id),
        }
    def get_revenue_by_category(self, org_id: int):
        return self.repo.get_revenue_by_category(org_id)


    def get_revenue_by_payment_method(self, org_id: int):
        return self.repo.get_revenue_by_payment_method(org_id)


    def get_monthly_revenue(self, org_id: int):
        return self.repo.get_monthly_revenue(org_id)
    
    def get_customer_growth(self, org_id: int):
        return self.repo.get_customer_growth(org_id)


    def get_average_customer_spend(self, org_id: int):
        return {
        "average_spend":
            self.repo.get_average_customer_spend(org_id)
    }


    def get_purchase_frequency(self, org_id: int):
        return {
        "average_purchase_frequency":
            self.repo.get_average_purchase_frequency(org_id)
    }

    def get_retention_summary(self, org_id: int):

        return self.repo.get_retention_summary(org_id)
    
    def get_top_customers(self, org_id: int):
        return self.repo.get_top_customers(org_id)


    def get_top_products(self, org_id: int):
        return self.repo.get_top_products(org_id)


    def get_top_categories(self, org_id: int):
        return self.repo.get_top_categories(org_id)


    def get_top_cities(self, org_id: int):
        return self.repo.get_top_cities(org_id)


    def get_top_states(self, org_id: int):
        return self.repo.get_top_states(org_id)
    
    def get_dashboard(self, org_id: int):

        return {

            "summary":
                self.get_dashboard_summary(org_id),

            "revenue": {

                "monthly":
                    self.get_monthly_revenue(org_id),

                "by_category":
                    self.get_revenue_by_category(org_id),

                "by_payment_method":
                    self.get_revenue_by_payment_method(org_id),

            },

            "customers": {

                "growth":
                    self.get_customer_growth(org_id),

                "average_spend":
                    self.get_average_customer_spend(org_id),

                "purchase_frequency":
                    self.get_purchase_frequency(org_id),

                "retention":
                    self.get_retention_summary(org_id),

            },

            "insights": {

                "top_customers":
                    self.get_top_customers(org_id),

                "top_products":
                    self.get_top_products(org_id),

                "top_categories":
                    self.get_top_categories(org_id),

                "top_cities":
                    self.get_top_cities(org_id),

                "top_states":
                    self.get_top_states(org_id),

            }

        }