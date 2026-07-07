from pydantic import BaseModel
from datetime import date
from typing import List


class DashboardSummary(BaseModel):
    total_customers: int
    active_customers: int

    total_transactions: int

    total_revenue: float

    average_order_value: float

    average_purchase_frequency: float


class RevenueCategory(BaseModel):
    category: str
    revenue: float


class RevenuePaymentMethod(BaseModel):
    payment_method: str
    revenue: float


class MonthlyRevenue(BaseModel):
    month: str
    revenue: float


class RevenueByCategory(BaseModel):
    category: str
    revenue: float


class RevenueByPaymentMethod(BaseModel):
    payment_method: str
    revenue: float


class RevenueTrend(BaseModel):
    period: str
    revenue: float

class CustomerGrowth(BaseModel):
    period: str
    new_customers: int


class CustomerSpend(BaseModel):
    average_spend: float


class PurchaseFrequency(BaseModel):
    average_purchase_frequency: float

class RetentionSummary(BaseModel):
    total_customers: int
    repeat_customers: int
    one_time_customers: int
    retention_rate: float
    repeat_purchase_rate: float

class TopCustomer(BaseModel):
    customer_id: int
    customer_name: str
    total_spent: float


class TopProduct(BaseModel):
    product_name: str
    revenue: float
    quantity_sold: int


class TopCategory(BaseModel):
    category: str
    revenue: float


class TopLocation(BaseModel):
    location: str
    customers: int

from typing import List


class RevenueDashboard(BaseModel):
    monthly: List[RevenueTrend]
    by_category: List[RevenueByCategory]
    by_payment_method: List[RevenueByPaymentMethod]


class CustomerDashboard(BaseModel):
    growth: List[CustomerGrowth]
    average_spend: CustomerSpend
    purchase_frequency: PurchaseFrequency
    retention: RetentionSummary


class InsightDashboard(BaseModel):
    top_customers: List[TopCustomer]
    top_products: List[TopProduct]
    top_categories: List[TopCategory]
    top_cities: List[TopLocation]
    top_states: List[TopLocation]


class DashboardResponse(BaseModel):
    summary: DashboardSummary
    revenue: RevenueDashboard
    customers: CustomerDashboard
    insights: InsightDashboard