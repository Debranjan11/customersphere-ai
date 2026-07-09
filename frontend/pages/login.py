import streamlit as st

from services.auth_service import auth_service
from utils.session import session


def render():

    st.title("CustomerSphere AI")

    st.subheader("Sign In")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password",
    )

    if st.button(
        "Login",
        use_container_width=True,
    ):

        response = auth_service.login(
            email,
            password,
        )

        if response.status_code == 200:

            data = response.json()

            session.login(
                data["access_token"],
                data["user"],
            )

            st.success("Login Successful")

            st.rerun()

        else:

            st.error("Invalid credentials")