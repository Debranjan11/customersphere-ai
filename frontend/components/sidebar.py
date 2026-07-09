import streamlit as st

from utils.session import session


class Sidebar:

    MENU = {
        "📊 Dashboard": "Dashboard",
        "👥 Customers": "Customers",
        "💳 Transactions": "Transactions",
        "📈 Analytics": "Analytics",
        "🤖 Segmentation": "Segmentation",
    }

    @staticmethod
    def render():

        with st.sidebar:

            st.title("CustomerSphere AI")

            user = st.session_state.get("user")

            if user:

                st.success(
                    user.get(
                        "organization_name",
                        "Organization"
                    )
                )

                st.caption(
                    f"👤 {user.get('name')}"
                )

                st.caption(
                    f"🔑 {user.get('role')}"
                )
            st.divider()

            for label, page in Sidebar.MENU.items():

                if st.button(
                    label,
                    use_container_width=True,
                ):

                    st.session_state.current_page = page

            st.divider()

            if st.button(
                "🚪 Logout",
                use_container_width=True,
            ):

                session.logout()

                st.rerun()