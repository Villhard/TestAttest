"""Основной файл бота."""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from handlers import admin_handlers, user_handlers  # noqa # FIXME

from keyboard.menu import set_menu

logger = logging.getLogger(__name__)


async def main() -> None:
    """Создание и запуск бота."""
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting bot")

    storage: MemoryStorage = MemoryStorage()

    bot = Bot(token=config.bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)

    await set_menu(bot)

    # dp.include_router(admin_handlers.router)
    dp.include_router(user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
