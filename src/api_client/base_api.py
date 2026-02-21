import httpx

from config.settings import settings


class BaseAPIClient:
    def __init__(self):

        self.base_url = settings.API_BASE_URL
        self.token = None

    @property
    def headers(self):
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def login(self, username: str, password: str):
        endpoint = "/auth/login"
        payload = {"username": username, "password": password}

        async with httpx.AsyncClient(base_url=self.base_url, timeout=10.0) as client:
            try:
                response = await client.post(
                    endpoint, json=payload, headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                data = response.json()  # сохраняем в переменную
                self.token = data.get("access_token")  # сохраняем токен
                return data
            except httpx.HTTPStatusError as e:
                return {"error": f"Server returned {e.response.status_code}"}
            except Exception as e:
                return {"error": str(e)}

    async def _request(self, method: str, endpoint: str, **kwargs):
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.headers, timeout=10.0
        ) as client:
            try:
                response = await client.request(method, endpoint, **kwargs)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                return {"erorr": f"Server returned{e.response.status_code}"}
            except Exception as e:
                return {"error": str(e)}

    async def get_data(self, user_id: int):

        return await self._request("GET", f"/users/{user_id}")
