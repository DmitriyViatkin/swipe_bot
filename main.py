import asyncio
import logging
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from aiogram.utils.i18n import I18n, FSMI18nMiddleware
from aiogram import Bot, Dispatcher
from config.settings import infra_settings
from src.api_client.base_api import BaseAPIClient
from src.bot.authorization.handlers import router as main_router

i18n = I18n(path="src/localization", default_locale="ua", domain="messages")


async def main():
    logging.basicConfig(
        level=logging.INFO if not infra_settings.bot.DEBUG else logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    redis_client = Redis.from_url(infra_settings.redis.url, decode_response=True)
    storage = RedisStorage(redis_client)

    bot = Bot(token=infra_settings.bot.BOT_TOKEN)
    dp = Dispatcher(storage=storage)
    api = BaseAPIClient()
    i18n_middleware = FSMI18nMiddleware(i18n=i18n)
    i18n_middleware.setup(dp)

    logging.info(
        f"🚀 Бот запускається... Режим: {'DEBUG' if infra_settings.bot.DEBUG else 'PROD'}"
    )
    dp.include_router(main_router)
    try:
        await dp.start_polling(bot, api=api)
    finally:
        await redis_client.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
