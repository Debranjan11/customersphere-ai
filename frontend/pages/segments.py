import streamlit as st
import pandas as pd

from services.segmentation_service import (
    segmentation_service,
)

SEGMENT_NAMES = {

    "0": "Big Spenders",

    "1": "At Risk",

    "2": "Potential Loyalists",

    "3": "Loyal Customers",

    "4": "Champions",

}
# ============================================================
# Helper Functions
# ============================================================

def train_model(token):

    response = segmentation_service.train_model(
        token
    )

    if response.status_code != 200:

        st.error(
            "Model training failed."
        )

        return None

    return response.json()


def predict_segments(token):

    response = segmentation_service.predict_segments(
        token
    )

    if response.status_code != 200:

        st.error(
            "Prediction failed."
        )

        return None

    return response.json()

# ============================================================
# Training Summary
# ============================================================

def display_training_summary(result):

    st.subheader("📊 Model Training Summary")

    col1, col2 = st.columns(2)

    col1.metric(
        "Customers Processed",
        result["customers_processed"],
    )

    col2.metric(
        "Clusters Created",
        result["clusters"],
    )

    st.divider()

    st.subheader("📈 Segment Distribution")

    distribution = result.get(
        "cluster_distribution",
        {},
    )

    if not distribution:

        st.info(
            "No distribution available."
        )

        return

    segment_names = {

        "0": "Big Spenders",

        "1": "At Risk",

        "2": "Potential Loyalists",

        "3": "Loyal Customers",

        "4": "Champions",

    }

    total = sum(
        distribution.values()
    )

    table = []

    for cluster, customers in distribution.items():

        table.append(

            {

                "Segment": segment_names.get(
                    str(cluster),
                    f"Cluster {cluster}"
                ),

                "Customers": customers,

                "Percentage": round(

                    customers * 100 / total,

                    2,

                ),

            }

        )

    dataframe = pd.DataFrame(
        table
    )

    st.bar_chart(

        dataframe.set_index(
            "Segment"
        )["Customers"]

    )

    st.dataframe(

        dataframe,

        use_container_width=True,

        hide_index=True,

    )
# ============================================================
# Prediction Results
# ============================================================

def display_prediction_table(predictions):

    st.subheader("👥 Customer Segments")

    if not predictions:

        st.info(
            "No prediction data available."
        )

        return

    dataframe = pd.DataFrame(
        predictions
    )

    if "cluster" in dataframe.columns:

        dataframe["segment"] = dataframe[
            "cluster"
        ].astype(str).map(
            SEGMENT_NAMES
        )

    preferred_columns = [

        "customer_code",

        "name",

        "segment",

        "cluster",

        "recency",

        "frequency",

        "monetary",

    ]

    available_columns = [

        column

        for column in preferred_columns

        if column in dataframe.columns

    ]

    dataframe = dataframe[
    available_columns
    ]

# ---------------------------------------
# Segment Filter
# ---------------------------------------

    available_segments = set(
        dataframe["segment"].dropna().tolist()
    )
    SEGMENT_ORDER = [
        "Champions",
        "Loyal Customers",
        "Big Spenders",
        "Potential Loyalists",
        "At Risk",
    ]

    segments = [
        segment
        for segment in SEGMENT_ORDER
        if segment in available_segments
    ]

    selected_segment = st.selectbox(
        "Filter by Segment",
        ["All"] + segments,
    )

    if selected_segment != "All":

        dataframe = dataframe[
            dataframe["segment"] == selected_segment
        ]

        dataframe.columns = [

            column.replace(
                "_",
                " "
            ).title()

            for column in dataframe.columns

        ]

    st.dataframe(

        dataframe,

        use_container_width=True,

        hide_index=True,

    )

    st.caption(

        f"Showing "

        f"{len(dataframe)} "

        f"customer(s)"

    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Displayed Customers",
        len(dataframe),
    )

    col2.metric(
        "Available Segments",
        len(segments),
    )

    st.divider()

# ============================================================
# Segment Guide
# ============================================================

def display_segment_guide():

    st.divider()

    st.subheader("📖 Segment Guide")

    segment_info = [
        {
            "Segment": "🏆 Champions",
            "Description": (
                "Customers with recent purchases, "
                "high spending, and frequent transactions."
            ),
            "Recommended Action": (
                "Reward with loyalty programs, "
                "exclusive offers, and early access."
            ),
        },
        {
            "Segment": "❤️ Loyal Customers",
            "Description": (
                "Regular customers who purchase "
                "consistently over time."
            ),
            "Recommended Action": (
                "Maintain engagement through "
                "personalized communication."
            ),
        },
        {
            "Segment": "💰 Big Spenders",
            "Description": (
                "Customers who spend a lot "
                "but may not purchase frequently."
            ),
            "Recommended Action": (
                "Promote premium products "
                "and bundle offers."
            ),
        },
        {
            "Segment": "🌱 Potential Loyalists",
            "Description": (
                "Customers showing promising "
                "purchase behavior."
            ),
            "Recommended Action": (
                "Encourage repeat purchases "
                "through targeted discounts."
            ),
        },
        {
            "Segment": "⚠ At Risk",
            "Description": (
                "Customers who have not purchased "
                "for a long time."
            ),
            "Recommended Action": (
                "Launch re-engagement campaigns "
                "and win-back offers."
            ),
        },
    ]

    st.dataframe(
        segment_info,
        use_container_width=True,
        hide_index=True,
    )
# ============================================================
# Main Page
# ============================================================

def render():

    st.title("🤖 Customer Segmentation")

    token = st.session_state.access_token

    st.markdown(
        """
        Train the customer segmentation model
        and predict customer segments using
        Machine Learning.
        """
    )

    st.divider()

    col1, col2 = st.columns(2)

    # -----------------------------------
    # Train Model
    # -----------------------------------

    with col1:

        if st.button(
            "🚀 Train Model",
            use_container_width=True,
        ):
            with st.spinner("Training machine learning model..."):
                result = train_model(
                    token
                )

            if result:

                st.session_state.training_result = result

                st.success(
                    "Model trained successfully."
                )

    # -----------------------------------
    # Predict Segments
    # -----------------------------------

    with col2:

        if st.button(
            "🔍 Predict Segments",
            use_container_width=True,
        ):
            with st.spinner("Predicting customer segments..."):
                predictions = predict_segments(
                    token
                )

            if predictions:

                st.session_state.segment_predictions = (
                    predictions
                )

                st.success(
                    "Segments predicted successfully."
                )

    st.divider()

    if "training_result" in st.session_state:

        display_training_summary(
            st.session_state.training_result
        )
    # -----------------------------------
    # Prediction Summary
    # -----------------------------------

    if "segment_predictions" in st.session_state:

        display_prediction_table(

        st.session_state.segment_predictions

    )
        
        display_segment_guide()