"""The bot."""
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from config import config
from data import lexicon_eng, lexicon_rus
from handlers import old_user_handlers
from handlers import admin_handlers


async def main() -> None:
    """Start the bot."""
    lexicon = lexicon_rus if config.language == "rus" else lexicon_eng
    logger.info(f"{lexicon.LOGS['starting bot']}")

    storage: MemoryStorage = MemoryStorage()

    bot = Bot(token=config.bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)

    dp.include_router(admin_handlers.router)
    dp.include_router(old_user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
