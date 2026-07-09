import streamlit as st


class ResponseHandler:

    @staticmethod
    def success(
        response,
        success_codes=(200, 201),
        message=None,
    ):
        """
        Returns True if response is successful.
        Displays optional success message.
        """

        if response.status_code in success_codes:

            if message:
                st.success(message)

            return True

        try:

            error = response.json()

            if isinstance(error, dict):

                detail = error.get(
                    "detail",
                    response.text,
                )

            else:

                detail = response.text

        except Exception:

            detail = response.text

        st.error(detail)

        return False

    @staticmethod
    def data(
        response,
        success_codes=(200,),
    ):
        """
        Returns JSON data if successful,
        otherwise shows error.
        """

        if response.status_code in success_codes:

            return response.json()

        try:

            error = response.json()

            if isinstance(error, dict):

                detail = error.get(
                    "detail",
                    response.text,
                )

            else:

                detail = response.text

        except Exception:

            detail = response.text

        st.error(detail)

        return None


response_handler = ResponseHandler()