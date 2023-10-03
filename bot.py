"""The bot."""
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from config import config
from data import lexicon_en, lexicon_ru
from handlers import old_user_handlers
from handlers import admin_handlers

lexicon = lexicon_ru if config.language == "ru" else lexicon_en


async def main() -> None:
    """Start the bot."""
    storage: MemoryStorage = MemoryStorage()

    bot = Bot(token=config.bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)

    dp.include_router(admin_handlers.router)
    dp.include_router(old_user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info(f"{lexicon.LOGS['starting bot']}")
    asyncio.run(main())
    logger.info(f"{lexicon.LOGS['stopping bot']}")
