import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config.settings import settings
from src.api_client.base_api import BaseAPIClient


async def main():

    logging.basicConfig(level=logging.INFO if not settings.DEBUG else logging.DEBUG)

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    api = BaseAPIClient()
    print(settings.API_BASE_URL)
    print(settings.BOT_TOKEN)
    print("BASE_URL:", repr(api.base_url))
    # Авторизация
    login_resp = await api.login("viatkindima@gmail.com", "string")
    if "error" in login_resp:
        print("Login failed:", login_resp)
        return
    print("Login success. Token:", api.token)

    # Пример получения данных пользователя через api
    user_data = await api.get_data(1)
    print("User data:", user_data)

    @dp.message(Command("profile"))
    async def get_profile(message: types.Message):
        data = await api.get_data(message.from_user.id)

        if "error" in data:
            await message.answer(f"Error API: {data['error']}")
        else:
            await message.answer(f"Data from server: {data}")

    print("🚀 Бот запускається...")
    print(f"Bot started DEBAG. Regim : {'DEBUG' if settings.DEBUG else 'PRODUCTION'}")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
