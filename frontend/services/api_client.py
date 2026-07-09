import requests

from config import config


class APIClient:

    def __init__(self):

        self.base_url = config.BASE_URL
        self.timeout = 30

    def _headers(self, token=None):

        headers = {
            "Content-Type": "application/json"
        }

        if token:
            headers["Authorization"] = f"Bearer {token}"

        return headers

    # ---------------------------
    # GET
    # ---------------------------
    def get(
        self,
        endpoint,
        token=None,
        params=None,
    ):

        return requests.get(
            f"{self.base_url}{endpoint}",
            headers=self._headers(token),
            params=params,
            timeout=self.timeout,
        )

    # ---------------------------
    # POST
    # ---------------------------
    def post(
        self,
        endpoint,
        data=None,
        token=None,
    ):

        return requests.post(
            f"{self.base_url}{endpoint}",
            json=data,
            headers=self._headers(token),
            timeout=self.timeout,
        )

    # ---------------------------
    # PUT
    # ---------------------------
    def put(
        self,
        endpoint,
        data=None,
        token=None,
    ):

        return requests.put(
            f"{self.base_url}{endpoint}",
            json=data,
            headers=self._headers(token),
            timeout=self.timeout,
        )

    # ---------------------------
    # DELETE
    # ---------------------------
    def delete(
        self,
        endpoint,
        token=None,
    ):

        return requests.delete(
            f"{self.base_url}{endpoint}",
            headers=self._headers(token),
            timeout=self.timeout,
        )


api_client = APIClient()