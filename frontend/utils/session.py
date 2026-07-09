import streamlit as st


class SessionManager:

    @staticmethod
    def initialize():

        defaults = {
            "authenticated": False,
            "access_token": None,
            "user": None,
            "current_page": "Dashboard",
        }

        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

    @staticmethod
    def login(
        token,
        user,
    ):

        st.session_state.authenticated = True
        st.session_state.access_token = token
        st.session_state.user = user

    @staticmethod
    def logout():

        keys = [
            "authenticated",
            "access_token",
            "user",
            "current_page",
        ]

        for key in keys:

            if key in st.session_state:

                del st.session_state[key]

        SessionManager.initialize()

    @staticmethod
    def is_authenticated():

        return st.session_state.get(
            "authenticated",
            False,
        )


session = SessionManager()