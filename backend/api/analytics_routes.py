from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.session import get_db

from backend.dependencies.auth import get_current_user

from backend.services.analytics_service import AnalyticsService

from backend.schemas.analytics import (
    DashboardSummary,
    RevenueByCategory,
    RevenueByPaymentMethod,
    RevenueTrend,
)
from backend.schemas.analytics import (
    CustomerGrowth,
    CustomerSpend,
    PurchaseFrequency,
)
from backend.schemas.analytics import (
    TopCustomer,
    TopProduct,
    TopCategory,
    TopLocation,
)
from backend.schemas.analytics import RetentionSummary

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get(
    "/dashboard-summary",
    response_model=DashboardSummary
)
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    service = AnalyticsService(db)

    return service.get_dashboard_summary(
        current_user.org_id
    )
@router.get(
    "/revenue/category",
    response_model=list[RevenueByCategory]
)
def revenue_by_category(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = AnalyticsService(db)
    return service.get_revenue_by_category(current_user.org_id)

@router.get(
    "/revenue/payment-method",
    response_model=list[RevenueByPaymentMethod]
)
def revenue_by_payment_method(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = AnalyticsService(db)
    return service.get_revenue_by_payment_method(current_user.org_id)

@router.get(
    "/revenue/monthly",
    response_model=list[RevenueTrend]
)
def monthly_revenue(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = AnalyticsService(db)
    return service.get_monthly_revenue(current_user.org_id)

#customer growth
@router.get(
    "/customers/growth",
    response_model=list[CustomerGrowth]
)
def customer_growth(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    service = AnalyticsService(db)

    return service.get_customer_growth(
        current_user.org_id
    )

#average speed
@router.get(
    "/customers/average-spend",
    response_model=CustomerSpend
)
def average_spend(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    service = AnalyticsService(db)

    return service.get_average_customer_spend(
        current_user.org_id
    )

#purchase frequency
@router.get(
    "/customers/purchase-frequency",
    response_model=PurchaseFrequency
)
def purchase_frequency(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    service = AnalyticsService(db)

    return service.get_purchase_frequency(
        current_user.org_id
    )

#retention service
@router.get(
    "/customers/retention",
    response_model=RetentionSummary
)
def retention_summary(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    service = AnalyticsService(db)

    return service.get_retention_summary(
        current_user.org_id
    )

#top customers
@router.get(
    "/insights/top-customers",
    response_model=list[TopCustomer]
)
def top_customers(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = AnalyticsService(db)
    return service.get_top_customers(current_user.org_id)

#top products
@router.get(
    "/insights/top-products",
    response_model=list[TopProduct]
)
def top_products(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = AnalyticsService(db)
    return service.get_top_products(current_user.org_id)

#top categoris
@router.get(
    "/insights/top-categories",
    response_model=list[TopCategory]
)
def top_categories(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = AnalyticsService(db)
    return service.get_top_categories(current_user.org_id)

#top cities
@router.get(
    "/insights/top-cities",
    response_model=list[TopLocation]
)
def top_cities(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = AnalyticsService(db)
    return service.get_top_cities(current_user.org_id)

#top states
@router.get(
    "/insights/top-states",
    response_model=list[TopLocation]
)
def top_states(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = AnalyticsService(db)
    return service.get_top_states(current_user.org_id)

from backend.schemas.analytics import DashboardResponse

@router.get(
    "/dashboard",
    response_model=DashboardResponse
)
def analytics_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    service = AnalyticsService(db)

    return service.get_dashboard(
        current_user.org_id
    )