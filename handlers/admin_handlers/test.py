import re

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery
from loguru import logger

from config import lexicon
from handlers.admin_handlers.states import FSMCreateTest
from keyboard import keyboard_builder as kb
from database import admin_connect as db
from utils import admin_utils as utils

router = Router()


@router.callback_query(F.data == "add_test", StateFilter(default_state))
async def call_add_test(callback: CallbackQuery, state: FSMContext):
    """Start create test"""

    # DEBUG LOG
    logger.debug(
        f"{lexicon.LOGS['add test'].format(admin_id=callback.from_user.id)}"
    )

    await callback.message.edit_text(text=f"{lexicon.MESSAGES['add test']}")
    await state.set_state(FSMCreateTest.title)


@router.callback_query(
    lambda call: re.fullmatch(r"confirm_delete_test_\d+", call.data),
    StateFilter(default_state),
)
async def call_confirm_delete_test(callback: CallbackQuery):
    """Confirm delete test"""
    test_id = int(callback.data.split("_")[3])
    keyboard = kb.create_confirm_keyboard(
        callback_yes=f"delete_test_{test_id}",
        callback_no=f"test_{test_id}",
    )

    # DEBUG LOG
    logger.debug(
        f"{lexicon.LOGS['confirm delete test'].format(admin_id=callback.from_user.id, test_id=test_id)}"
    )

    await callback.message.edit_text(
        text=f"{lexicon.MESSAGES['confirm delete test']}",
        reply_markup=keyboard,
    )


@router.callback_query(
    lambda call: re.fullmatch(r"delete_test_\d+", call.data),
    StateFilter(default_state),
)
async def call_delete_test(callback: CallbackQuery):
    """Delete test"""
    test_id = int(callback.data.split("_")[2])
    utils.delete_test_dir(test_id)
    db.delete_test_by_id(test_id)
    keyboard = kb.create_tests_menu_keyboard(
        tests=db.get_tests(),
        is_admin=True,
    )

    # DEBUG LOG
    logger.debug(
        f"{lexicon.LOGS['delete test'].format(admin_id=callback.from_user.id, test_id=test_id)}"
    )

    await callback.message.edit_text(
        text=f"{lexicon.MESSAGES['delete test']}",
        reply_markup=keyboard
    )