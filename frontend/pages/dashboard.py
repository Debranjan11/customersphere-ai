import streamlit as st


def render():

    st.title("🏠 CustomerSphere AI")

    st.markdown(
        """
        ### Welcome to your Customer Intelligence Platform

        Manage customers, analyze transactions, generate
        AI-powered insights, and monitor customer behavior
        from one place.
        """
    )

    st.divider()

    # ===================================================
    # User Information
    # ===================================================

    user = st.session_state.get(
        "user",
        {}
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "👤 User",
            user.get(
                "name",
                "Administrator",
            ),
        )

    with col2:

        st.metric(
            "🏢 Organization",
            user.get(
                "organization",
                "CustomerSphere",
            ),
        )

    with col3:

        st.metric(
            "🔐 Role",
            user.get(
                "role",
                "Admin",
            ),
        )

    st.divider()

    # ===================================================
    # Quick Navigation
    # ===================================================

    st.subheader("🚀 Quick Navigation")

    row1 = st.columns(2)

    with row1[0]:

        st.info(
            """
### 👥 Customer Management

Create, update and manage customers.
"""
        )

    with row1[1]:

        st.info(
            """
### 💳 Transaction Management

Manage customer purchases and sales.
"""
        )

    row2 = st.columns(2)

    with row2[0]:

        st.info(
            """
### 📈 Analytics Dashboard

View KPIs and business insights.
"""
        )

    with row2[1]:

        st.info(
            """
### 🤖 Customer Segmentation

Train ML models and predict customer groups.
"""
        )

    st.divider()

    # ===================================================
    # Platform Features
    # ===================================================

    st.subheader("✨ Platform Features")

    features = [

        "✅ Multi-Tenant Architecture",

        "✅ JWT Authentication",

        "✅ Customer Management",

        "✅ Transaction Management",

        "✅ Business Analytics",

        "✅ Customer Segmentation",

        "🚧 Churn Prediction (Module 9)",

        "🚧 Customer Lifetime Value (Module 10)",

        "🚧 Next Purchase Prediction (Module 11)",

        "🚧 AI Business Insights (Module 12)",

    ]

    for feature in features:

        st.write(feature)

    st.divider()

    st.success(
        "CustomerSphere AI is running successfully."
    )