import streamlit as st

from utils.session import session

from components.sidebar import Sidebar

from pages import (
    login,
    dashboard,
    customers,
    transactions,
    analytics,
    segments,
)


st.set_page_config(
    page_title="CustomerSphere AI",
    page_icon="🤖",
    layout="wide",
)

session.initialize()

if not session.is_authenticated():

    login.render()

else:

    Sidebar.render()

    page = st.session_state.current_page

    if page == "Dashboard":

        dashboard.render()

    elif page == "Customers":

        customers.render()

    elif page == "Transactions":

        transactions.render()

    elif page == "Analytics":

        analytics.render()

    elif page == "Segmentation":

        segments.render()