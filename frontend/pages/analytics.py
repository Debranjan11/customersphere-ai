import streamlit as st
import pandas as pd

from services.analytics_service import (
    analytics_service,
)


# ============================================================
# Helper Functions
# ============================================================

def load_dashboard_summary(token):

    response = analytics_service.get_dashboard_summary(
        token
    )

    if response.status_code != 200:

        st.error(
            "Unable to load dashboard summary."
        )

        return None

    return response.json()


def display_kpi_cards(summary):

    st.subheader("📊 Business Overview")

    row1 = st.columns(3)

    row1[0].metric(
        "💰 Total Revenue",
        f"₹ {summary['total_revenue']:,.2f}"
    )

    row1[1].metric(
        "👥 Total Customers",
        summary["total_customers"]
    )

    row1[2].metric(
        "🟢 Active Customers",
        summary["active_customers"]
    )

    row2 = st.columns(3)

    row2[0].metric(
        "💳 Transactions",
        summary["total_transactions"]
    )

    row2[1].metric(
        "🧾 Avg Order Value",
        f"₹ {summary['average_order_value']:,.2f}"
    )

    row2[2].metric(
        "🔄 Purchase Frequency",
        round(
            summary["average_purchase_frequency"],
            2,
        )
    )
# ============================================================
# Main Page
# ============================================================

def render():

    st.title("📈 Analytics Dashboard")

    token = st.session_state.access_token

    with st.spinner("Loading analytics dashboard..."):
        dashboard_response = analytics_service.get_dashboard(
            token
        )

    if dashboard_response.status_code != 200:

        st.error(
            "Unable to load analytics dashboard."
        )

        return

    dashboard = dashboard_response.json()

    summary = dashboard["summary"]

    display_kpi_cards(summary)

    st.divider()

    display_revenue_by_category(
        dashboard["revenue"]["by_category"]
    )

    st.divider()

    display_revenue_by_payment(
        dashboard["revenue"]["by_payment_method"]
    )

    st.divider()

    display_monthly_revenue(
        dashboard["revenue"]["monthly"]
    )
    st.divider()

    display_customer_growth(
        dashboard["customers"]["growth"]
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        display_average_spend(
            dashboard["customers"]["average_spend"]
        )

    with col2:

        display_purchase_frequency(
            dashboard["customers"]["purchase_frequency"]
        )

    st.divider()

    display_retention(
        dashboard["customers"]["retention"]
    )

    st.divider()

    display_top_customers(
        dashboard["insights"]["top_customers"]
    )

    st.divider()

    display_top_products(
        dashboard["insights"]["top_products"]
    )

    st.divider()

    display_top_categories(
        dashboard["insights"]["top_categories"]
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        display_top_cities(
            dashboard["insights"]["top_cities"]
        )

    with col2:

        display_top_states(
            dashboard["insights"]["top_states"]
        )

# ============================================================
# Business Insights
# ============================================================

def display_top_customers(customers):

    st.subheader("🏆 Top Customers")

    if not customers:

        st.info("No customer insights available.")

        return

    dataframe = pd.DataFrame(customers)

    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=True,
    )


def display_top_products(products):

    st.subheader("📦 Top Products")

    if not products:

        st.info("No product insights available.")

        return

    dataframe = pd.DataFrame(products)

    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=True,
    )


def display_top_categories(categories):

    st.subheader("🗂 Top Categories")

    if not categories:

        st.info("No category insights available.")

        return

    dataframe = pd.DataFrame(categories)

    dataframe = dataframe.set_index("category")

    st.bar_chart(dataframe)


def display_top_cities(cities):

    st.subheader("🏙 Top Cities")

    if not cities:

        st.info("No city insights available.")

        return

    dataframe = pd.DataFrame(cities)

    dataframe = dataframe.set_index("location")

    st.bar_chart(dataframe)


def display_top_states(states):

    st.subheader("🗺 Top States")

    if not states:

        st.info("No state insights available.")

        return

    dataframe = pd.DataFrame(states)

    dataframe = dataframe.set_index("location")

    st.bar_chart(dataframe)

# ============================================================
# Revenue Analytics
# ============================================================

def display_revenue_by_category(categories):

    st.subheader("📦 Revenue by Category")

    if not categories:

        st.info("No category data available.")

        return

    dataframe = pd.DataFrame(categories)

    dataframe = dataframe.set_index("category")

    st.bar_chart(dataframe)


def display_revenue_by_payment(payment_methods):

    st.subheader("💳 Revenue by Payment Method")

    if not payment_methods:

        st.info("No payment data available.")

        return

    dataframe = pd.DataFrame(payment_methods)

    dataframe = dataframe.set_index("payment_method")

    st.bar_chart(dataframe)


def display_monthly_revenue(monthly):

    st.subheader("📈 Monthly Revenue")

    if not monthly:

        st.info("No monthly revenue available.")

        return

    dataframe = pd.DataFrame(monthly)

    dataframe = dataframe.set_index("period")

    st.line_chart(dataframe)

# ============================================================
# Customer Analytics
# ============================================================

def display_customer_growth(growth):

    st.subheader("👥 Customer Growth")

    if not growth:

        st.info("No customer growth data available.")

        return

    dataframe = pd.DataFrame(growth)

    dataframe = dataframe.set_index("period")

    st.line_chart(dataframe)


def display_average_spend(spend):

    st.subheader("💰 Average Customer Spend")

    col1 = st.columns(1)[0]

    col1.metric(
        "Average Spend",
        f"₹ {spend['average_spend']:,.2f}"
    )


def display_purchase_frequency(frequency):

    st.subheader("🔄 Purchase Frequency")

    col1 = st.columns(1)[0]

    col1.metric(
        "Average Purchases",
        round(
            frequency["average_purchase_frequency"],
            2,
        )
    )


def display_retention(retention):

    st.subheader("📊 Customer Retention")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Retention Rate",
        f"{retention['retention_rate']:.2f}%"
    )

    col2.metric(
        "Repeat Customers",
        retention["repeat_customers"]
    )

    col3.metric(
        "One-Time Customers",
        retention["one_time_customers"]
    )