import httpx
from config.settings import infra_settings
import jwt

HTTP_CLIENT_KWARGS = {
    "timeout": 10.0,
    "follow_redirects": True,
    "verify": False,  #
}


class BaseAPIClient:
    def __init__(self):
        self.base_url = infra_settings.bot.API_BASE_URL
        self.user_tokens = {}

    def _decode_user_id(self, token: str) -> int | str | None:
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            print(f"DEBUG: JWT Payload -> {payload}")
            return payload.get("user_id") or payload.get("sub") or payload.get("id")
        except Exception as e:
            print(f"DECODE ERROR: {e}")
            return None

    async def login(self, username: str, password: str, telegram_id: int):
        endpoint = "/auth/login"
        payload = {"username": username, "password": password}
        async with httpx.AsyncClient(
            base_url=self.base_url, **HTTP_CLIENT_KWARGS
        ) as client:
            try:
                response = await client.post(
                    endpoint, json=payload, headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                data = response.json()
                access_token = data.get("access_token")
                if access_token:
                    self.user_tokens[telegram_id] = access_token
                return data
            except Exception as e:
                return {"error": str(e)}

    async def _request(self, method: str, endpoint: str, token: str = None, **kwargs):
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        async with httpx.AsyncClient(
            base_url=self.base_url, **HTTP_CLIENT_KWARGS
        ) as client:
            try:
                response = await client.request(
                    method, endpoint, headers=headers, **kwargs
                )
                if response.status_code == 422:
                    print(f"422 ERROR DETAIL: {response.json()}")
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                return {"error": f"Server returned {e.response.status_code}"}
            except Exception as e:
                return {"error": str(e)}

    async def get_user_data(self, user_id: int, token: str):
        return await self._request(
            method="GET", endpoint=f"/users/user/{user_id}", token=token
        )

    async def registration(self, **kwargs):
        async with httpx.AsyncClient(
            base_url=self.base_url, **HTTP_CLIENT_KWARGS
        ) as client:
            try:
                response = await client.post("/users/user/create/", json=kwargs)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                return {"error": str(e)}

    async def create_adverts(self, token: str, **kwargs):
        print(f"DEBUG KWARGS: {kwargs}")
        return await self._request(
            method="POST", endpoint="/adverts/advert", token=token, json=kwargs
        )

    async def get_list_adverts(self):
        return await self._request(method="GET", endpoint="/adverts/adverts")

    async def get_my_adverts(self, token: str, user_id: int):
        return await self._request(
            method="GET", endpoint=f"/adverts/adverts/my/{user_id}", token=token
        )  # ✅ виправлено
