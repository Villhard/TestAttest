"""The bot."""
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from config import config, lexicon
from handlers import admin_handlers, user_handlers


async def main() -> None:
    """Start the bot."""
    storage: MemoryStorage = MemoryStorage()

    bot = Bot(token=config.bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)

    dp.include_router(admin_handlers.router)
    dp.include_router(user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info(lexicon.LOGS["starting bot"])
    asyncio.run(main())
    logger.info(lexicon.LOGS["stopping bot"])
