from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger

from config import config
from data import lexicon_eng, lexicon_rus
from keyboard import keyboard_builder as kb

router = Router()
lexicon = lexicon_rus if config.language == "rus" else lexicon_eng


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Greeting admin"""
    logger.info(f"{lexicon.LOGS['greeting admin']}")
    keyboard = kb.create_main_menu_keyboard(is_admin=True)
    return await message.answer(
        text=lexicon.MESSAGES["greeting admin"],
        reply_markup=keyboard,
    )
