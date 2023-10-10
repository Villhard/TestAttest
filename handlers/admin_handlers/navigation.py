import re

from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from loguru import logger

from config import lexicon
from keyboard import keyboard_builder as kb
from database import admin_connect as db

router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message):
    """Greeting admin"""
    admin_id = message.from_user.id

    # DEBUG LOG
    logger.debug(
        f"{lexicon.LOGS['greeting admin'].format(admin_id=admin_id)}"
    )

    keyboard = kb.create_main_menu_keyboard(is_admin=True)
    await message.answer(
        text=lexicon.MESSAGES["greeting admin"],
        reply_markup=keyboard,
    )
    await message.delete()


@router.callback_query(F.data == "main menu", StateFilter(default_state))
async def call_main_menu(callback: CallbackQuery):
    """Main menu."""
    admin_id = callback.from_user.id

    # DEBUG LOG
    logger.debug(
        f"{lexicon.LOGS['main menu'].format(admin_id=admin_id)}"
    )

    keyboard = kb.create_main_menu_keyboard(is_admin=True)
    await callback.message.edit_text(
        text=lexicon.MESSAGES["main menu"],
        reply_markup=keyboard,
    )


@router.callback_query(F.data == "tests", StateFilter(default_state))
async def call_tests(callback: CallbackQuery):
    """Tests menu."""
    admin_id = callback.from_user.id

    # DEBUG LOG
    logger.debug(
        f"{lexicon.LOGS['tests'].format(admin_id=admin_id)}"
    )

    tests = db.get_tests()
    keyboard = kb.create_tests_menu_keyboard(tests=tests, is_admin=True)
    await callback.message.edit_text(
        text=lexicon.MESSAGES["tests"],
        reply_markup=keyboard,
    )


@router.callback_query(F.data == "users", StateFilter(default_state))
async def call_users(callback: CallbackQuery):
    """Users menu."""
    admin_id = callback.from_user.id

    # DEBUG LOG
    logger.debug(
        f"{lexicon.LOGS['users'].format(admin_id=admin_id)}"
    )

    users = db.get_users()
    keyboard = kb.create_users_menu_keyboard(users=users)
    await callback.message.edit_text(
        text=lexicon.MESSAGES["users"],
        reply_markup=keyboard,
    )


@router.callback_query(
    lambda call: re.fullmatch(r"test \d+", call.data),
    StateFilter(default_state),
)
async def call_test(callback: CallbackQuery):
    """Test menu."""
    test_id = int(callback.data.split()[1])
    admin_id = callback.from_user.id

    # DEBUG LOG
    logger.debug(
        f"{lexicon.LOGS['test'].format(admin_id=admin_id, test_id=test_id)}"
    )

    test = db.get_test_by_id(test_id=test_id)
    questions = db.get_questions_by_test_id(test_id=test_id)
    keyboard = kb.create_test_menu_keyboard(
        test=test, questions=questions, is_publish=test.is_publish
    )
    text = f"<b>{test.title}</b>\n{test.description}"

    if test.is_publish:
        statistics = db.get_statistics_by_test_id(test_id=test_id)
        text += f"{lexicon.MESSAGES['test statistics'].format(statistics=statistics)}"

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
    )


@router.callback_query(
    lambda call: re.fullmatch(r"question_\d+", call.data),
    StateFilter(default_state),
)
async def call_question(callback: CallbackQuery):
    """Question menu"""
    question_id = int(callback.data.split("_")[1])
    admin_id = callback.from_user.id

    # DEBUG LOG
    logger.debug(
        f"{lexicon.LOGS['question'].format(admin_id=admin_id, question_id=question_id)}"
    )

    question, answers = db.get_question_by_id(question_id=question_id)
    keyboard = kb.create_question_menu_keyboard(
        answers=answers,
    )

    await callback.message.edit_text(
        text=question.text,
        reply_markup=keyboard,
    )


@router.callback_query(
    lambda call: re.fullmatch(r"user_\d+", call.data),
    StateFilter(default_state),
)
async def call_user(callback: CallbackQuery):
    """User menu"""
    user_id = int(callback.data.split("_")[1])
    admin_id = callback.from_user.id

    # DEBUG LOG
    logger.debug(
        f"{lexicon.LOGS['user'].format(admin_id=admin_id, user_id=user_id)}"
    )

    user = db.get_user_by_id(user_id=user_id)
    results = db.get_results_by_user_id(user_id=user_id)
    keyboard = kb.create_user_menu_keyboard(user=user)

    await callback.message.edit_text(
        text=lexicon.MESSAGES["user statistics"].format(user=user, results=results),
        reply_markup=keyboard,
    )


@router.callback_query(
    lambda call: re.fullmatch(r"result_\d+", call.data),
    StateFilter(default_state),
)
async def call_result(call: CallbackQuery):
    """Result menu"""
    result_id = int(call.data.split("_")[1])
    admin_id = call.from_user.id

    # DEBUG LOG
    logger.debug(
        f"{lexicon.LOGS['result'].format(admin_id=admin_id, result_id=result_id)}"
    )

    result = db.get_result_by_id(result_id=result_id)
    test = db.get_test_by_id(result.test_id)
    result_data = db.get_result_data_by_result(result)
    text = f"<b>{test.title}</b>\n\n"
    text += "\n".join(
        [
            f"<u>{data[0]}</u>\n<s>{data[2]}</s>\n{data[1]}\n"
            for data in result_data
        ]
    )
    keyboard = kb.create_back_button_keyboard(
        callback_data=f"user_{result.user_id}",
    )

    await call.message.edit_text(
        text=text,
        reply_markup=keyboard,
    )
