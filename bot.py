import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import config
from handlers import admin_handlers, user_handlers

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting bot")

    bot = Bot(token=config.token, parse_mode="HTML")
    dp = Dispatcher()

    dp.include_router(admin_handlers.router)
    dp.include_router(user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
