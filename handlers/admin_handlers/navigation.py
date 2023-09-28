from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from loguru import logger

from config import config
from data import lexicon_eng, lexicon_rus
from keyboard import keyboard_builder as kb
from database import admin_connect as db

router = Router()
lexicon = lexicon_rus if config.language == "rus" else lexicon_eng


@router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message):
    """Greeting admin"""
    logger.debug(
        f"{lexicon.LOGS['greeting admin'].format(admin_id=message.from_user.id)}"
    )
    keyboard = kb.create_main_menu_keyboard(is_admin=True)
    await message.delete()
    return await message.answer(
        text=lexicon.MESSAGES["greeting admin"],
        reply_markup=keyboard,
    )


@router.callback_query(F.data == "main menu", StateFilter(default_state))
async def call_main_menu(callback: CallbackQuery):
    """Main menu."""
    logger.debug(f"{lexicon.LOGS['main menu'].format(admin_id=callback.from_user.id)}")
    keyboard = kb.create_main_menu_keyboard(is_admin=True)
    return await callback.message.edit_text(
        text=lexicon.MESSAGES["main menu"],
        reply_markup=keyboard,
    )


@router.callback_query(F.data == "tests", StateFilter(default_state))
async def call_tests(callback: CallbackQuery):
    """Tests menu."""
    logger.debug(f"{lexicon.LOGS['tests'].format(admin_id=callback.from_user.id)}")
    tests = db.get_tests()
    keyboard = kb.create_tests_menu_keyboard(tests=tests, is_admin=True)
    return await callback.message.edit_text(
        text=lexicon.MESSAGES["tests"],
        reply_markup=keyboard,
    )


@router.callback_query(F.data == "users", StateFilter(default_state))
async def call_users(callback: CallbackQuery):
    """Users menu."""
    logger.debug(f"{lexicon.LOGS['users'].format(admin_id=callback.from_user.id)}")
    users = db.get_users()
    keyboard = kb.create_users_menu_keyboard(users=users)
    return await callback.message.edit_text(
        text=lexicon.MESSAGES["users"],
        reply_markup=keyboard,
    )
