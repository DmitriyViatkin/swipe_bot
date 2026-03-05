import httpx
from config.settings import infra_settings
import jwt


class BaseAPIClient:
    def __init__(self):
        self.base_url = infra_settings.bot.API_BASE_URL
        self.user_tokens = {}

    def _decode_user_id(self, token: str) -> int | str | None:
        """Вспомогательный метод для получения ID из JWT"""
        try:
            payload = jwt.decode(token, options={"verify_signature": False})

            print(f"DEBUG: JWT Payload -> {payload}")

            user_id = payload.get("user_id") or payload.get("sub") or payload.get("id")

            return user_id
        except Exception as e:
            print(f"DECODE ERROR: {e}")
            return None

    async def login(self, username: str, password: str, telegram_id: int):
        endpoint = "/auth/login"
        payload = {"username": username, "password": password}

        async with httpx.AsyncClient(base_url=self.base_url, timeout=10.0) as client:
            try:
                response = await client.post(
                    endpoint, json=payload, headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()

                data = response.json()

                access_token = data.get("access_token")

                if access_token:
                    self.user_tokens[telegram_id] = access_token  # 🔥 сохраняем

                return data

            except Exception as e:
                return {"error": str(e)}

    async def _request(self, method: str, endpoint: str, token: str = None, **kwargs):
        # Формируем заголовки локально
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        async with httpx.AsyncClient(base_url=self.base_url, timeout=10.0) as client:
            try:
                response = await client.request(
                    method, endpoint, headers=headers, **kwargs
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                return {"error": f"Server returned {e.response.status_code}"}
            except Exception as e:
                return {"error": str(e)}

    async def get_user_data(self, user_id: int, token: str):
        """Получение профиля пользователя"""
        endpoint = f"/users/user/{user_id}"
        return await self._request(method="GET", endpoint=endpoint, token=token)

    async def registration(self, **kwargs):

        endpoint = "/users/user/create/"
        async with httpx.AsyncClient(base_url=self.base_url, timeout=10.0) as client:
            try:
                response = await client.post(endpoint, json=kwargs)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                return {"error": str(e)}

    async def create_adverts(self, token: str, **kwargs):
        print(f"DEBUG KWARGS: {kwargs}")
        endpoint = "/adverts/advert"
        return await self._request(
            method="POST", endpoint=endpoint, token=token, json=kwargs
        )

    async def get_list_adverts(self):

        endpoint = "adverts/adverts"
        return await self._request(
            method="GET",
            endpoint=endpoint,
        )
