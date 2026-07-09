from services.api_client import api_client


class AuthService:

    def login(
        self,
        email: str,
        password: str,
    ):

        payload = {
            "email": email,
            "password": password,
        }

        response = api_client.post(
            "/auth/login",
            data=payload,
        )

        return response

    def get_profile(
        self,
        token: str,
    ):

        response = api_client.get(
            "/auth/me",
            token=token,
        )

        return response


auth_service = AuthService()