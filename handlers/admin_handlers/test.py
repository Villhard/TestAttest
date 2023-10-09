import re

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery
from loguru import logger

from config import lexicon
from database import admin_connect as db
from handlers.admin_handlers.states import FSMCreateTest
from keyboard import keyboard_builder as kb
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
        text=f"{lexicon.MESSAGES['delete test']}", reply_markup=keyboard
    )


@router.callback_query(
    lambda call: re.fullmatch(r"confirm_publish_test_\d+", call.data),
    StateFilter(default_state),
)
async def call_confirm_publish_test(callback: CallbackQuery):
    """Confirm publish test"""
    test_id = int(callback.data.split("_")[3])
    keyboard = kb.create_confirm_keyboard(
        callback_yes=f"publish_test_{test_id}",
        callback_no=f"test_{test_id}",
    )

    # DEBUG LOG
    logger.debug(
        f"{lexicon.LOGS['confirm publish test'].format(admin_id=callback.from_user.id, test_id=test_id)}"
    )

    await callback.message.edit_text(
        text=f"{lexicon.MESSAGES['confirm publish test']}",
        reply_markup=keyboard,
    )


@router.callback_query(
    lambda call: re.fullmatch(r"publish_test_\d+", call.data),
    StateFilter(default_state),
)
async def call_publish_test(callback: CallbackQuery):
    """Publish test"""
    test_id = int(callback.data.split("_")[2])
    db.publish_test_by_id(test_id)
    keyboard = kb.create_tests_menu_keyboard(
        tests=db.get_tests(),
        is_admin=True,
    )

    # DEBUG LOG
    logger.debug(
        f"{lexicon.LOGS['publish test'].format(admin_id=callback.from_user.id, test_id=test_id)}"
    )

    await callback.message.edit_text(
        text=f"{lexicon.MESSAGES['publish test']}",
        reply_markup=keyboard,
    )


@router.callback_query(
    lambda call: re.fullmatch(r"edit_correct_answer_\d+_\d+", call.data),
    StateFilter(default_state),
)
async def call_edit_correct_answer(callback: CallbackQuery):
    """Edit correct answer"""
    question_id = int(callback.data.split("_")[3])
    answer_id = int(callback.data.split("_")[4])
    db.change_correct_answer(question_id, answer_id)
    question, answers = db.get_question_by_id(question_id)
    keyboard = kb.create_question_menu_keyboard(
        answers=answers,
    )

    # DEBUG LOG
    logger.debug(
        f"{lexicon.LOGS['edit correct answer'].format(admin_id=callback.from_user.id, question_id=question_id)}"
    )

    try:
        await callback.message.edit_text(
            text=question.text,
            reply_markup=keyboard,
        )
    except TelegramBadRequest:
        await callback.answer()


@router.callback_query(
    lambda call: re.fullmatch(r"delete_question_\d+", call.data),
    StateFilter(default_state),
)
async def call_delete_question(callback: CallbackQuery):
    """Delete question"""
    question_id = int(callback.data.split("_")[2])
    test = db.get_test_by_question_id(question_id)
    db.delete_question_by_id(question_id)
    keyboard = kb.create_test_menu_keyboard(
        test=test,
        questions=db.get_questions_by_test_id(test.id),
        is_publish=test.is_publish,
    )

    # DEBUG LOG
    logger.debug(
        f"{lexicon.LOGS['delete question'].format(admin_id=callback.from_user.id, question_id=question_id)}"
    )

    await callback.answer(
        text=f"{lexicon.MESSAGES['delete question']}",
    )
    await callback.message.edit_text(
        text=f"<b>{test.title}</b>\n{test.description}",
        reply_markup=keyboard,
    )