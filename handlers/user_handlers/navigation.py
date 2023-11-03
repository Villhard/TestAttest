import re

from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from config import lexicon
from database import user_connect as db
from handlers.user_handlers.states import FSMUserInputName
from keyboard import keyboard_builder as kb

router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message, state: FSMContext):
    """Greeting user"""
    user = db.get_user(message.from_user.id)
    if user:
        keyboard = kb.create_main_menu_keyboard(
            is_admin=False,
        )
        await message.answer(
            text=lexicon.MESSAGES["greeting user"].format(name=user.name),
            reply_markup=keyboard,
        )
    else:
        await message.answer(text=lexicon.MESSAGES["greeting stranger"])
        await state.set_state(FSMUserInputName.fullname)


@router.callback_query(F.data == "main_menu", StateFilter(default_state))
async def call_main_menu(callback: CallbackQuery):
    """Main menu"""
    keyboard = kb.create_main_menu_keyboard(
        is_admin=False,
    )
    await callback.message.edit_text(
        text=lexicon.MESSAGES["main menu"],
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(F.data == "tests", StateFilter(default_state))
async def call_tests(callback: CallbackQuery):
    """Tests menu"""
    user_tg_id = callback.from_user.id
    keyboard = kb.create_tests_menu_keyboard(
        tests=db.get_tests(
            tg_id=user_tg_id,
        ),
        is_admin=False,
    )
    await callback.message.edit_text(
        text=lexicon.MESSAGES["tests"],
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(
    lambda call: re.fullmatch(r"test_\d+", call.data),
    StateFilter(default_state),
)
async def call_test(callback: CallbackQuery):
    """Test menu"""
    test_id = int(callback.data.split("_")[1])
    test = db.get_test(test_id)
    keyboard = kb.create_confirm_keyboard(
        callback_yes=f"start_test_{test_id}",
        callback_no="tests",
        text_yes=lexicon.BUTTONS["test yes"],
        text_no=lexicon.BUTTONS["test no"],
    )
    await callback.message.edit_text(
        text=f"<b>{test.title}</b>\n\n{test.description}",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.message(
    F.text,
    StateFilter(FSMUserInputName.fullname),
    lambda msg: len(msg.text.split()) == 2,
)
async def process_input_name(message: Message, state: FSMContext):
    """Create user. Name and surname."""
    name, surname = message.text.title().split()
    keyboard = kb.create_main_menu_keyboard(
        is_admin=False,
    )
    await message.answer(
        text=lexicon.MESSAGES["greeting user"].format(name=name),
        reply_markup=keyboard,
    )
    await state.clear()


@router.message(F.text, StateFilter(FSMUserInputName.fullname))
async def process_incorrect_input_name(message: Message):
    """Incorrect input processing."""
    await message.answer(text=lexicon.MESSAGES["incorrect input"])
