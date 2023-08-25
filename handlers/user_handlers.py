"""User handlers."""
import re

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    FSInputFile,
    Message,
)

from database import user_connect
from keyboard import keyboard_builder

router = Router()


# ?============================================================================
# *========== МАШИНЫ СОСТОЯНИЙ ================================================
# ?============================================================================


class FSMUserInputName(StatesGroup):
    """Класс состояния ввода имени пользователя."""

    fullname = State()


class FSMTesting(StatesGroup):
    """Класс состояния прохождения теста."""

    answering = State()


# ?============================================================================
# *========== НАВИГАЦИЯ =======================================================
# ?============================================================================


@router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message, state: FSMContext) -> None:
    """Приветствие пользователя или запрос имени и фамилии."""
    user = user_connect.get_user(message.from_user.id)
    if user:
        keyboard = keyboard_builder.create_main_menu_keyboard(
            is_admin=False,
        )
        await message.answer(
            text=f"Здравствуйте, {user.name}!",
            reply_markup=keyboard,
        )
    else:
        await message.answer(
            text=(
                "Добро пожаловать в бота для тестирования!\n\n"
                "Введите ваше имя и фалимию"
            )
        )
        await state.set_state(FSMUserInputName.fullname)


@router.message(Command(commands="help"), StateFilter(default_state))
async def cmd_help(message: Message) -> None:
    """Помощь пользователю."""
    pass


@router.callback_query(F.data == "main_menu", StateFilter(default_state))
async def call_main_menu(callback: CallbackQuery) -> None:
    """Переход к главному меню."""
    keyboard = keyboard_builder.create_main_menu_keyboard(
        is_admin=False,
    )
    await callback.message.edit_text(
        text="Главное меню",
        reply_markup=keyboard,
    )


@router.callback_query(F.data == "tests", StateFilter(default_state))
async def call_tests(callback: CallbackQuery) -> None:
    """Переход к списку тестов."""
    user_tg_id = callback.from_user.id
    keyboard = keyboard_builder.create_tests_keyboard(
        tests=user_connect.get_tests(
            tg_id=user_tg_id,
        ),
        is_admin=False,
    )
    await callback.message.edit_text(
        text="Выберите тест",
        reply_markup=keyboard,
    )


@router.callback_query(
    lambda call: re.fullmatch(r"test_\d+", call.data),
    StateFilter(default_state),
)
async def call_test(callback: CallbackQuery) -> None:
    """Переход к тесту."""
    test_id = int(callback.data.split("_")[1])
    test = user_connect.get_test(test_id)
    photo = FSInputFile(f"img/test_{test_id}/default.jpg")
    await callback.message.answer_photo(
        photo=photo,
        caption=f"<b>{test.title}</b>\n\n{test.description}",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Начать",
                        callback_data=f"start_test_{test_id}",
                    )
                ]
            ]
        ),
    )
    await callback.answer()


# ?============================================================================
# *========== ПРОЦЕСС СОЗДАНИЯ ПОЛЬЗОВАТЕЛЯ ===================================
# ?============================================================================


@router.message(
    F.text,
    StateFilter(FSMUserInputName.fullname),
    lambda msg: len(msg.text.split()) == 2,
)
async def process_input_name(message: Message, state: FSMContext) -> None:
    """Получение имени и фамилии пользователя."""
    name, surname = message.text.title().split()
    user_connect.create_user(message.from_user.id, name, surname)
    keyboard = keyboard_builder.create_main_menu_keyboard(
        is_admin=False,
    )
    await message.answer(
        text="Вы успешно зарегистрировались!",
        reply_markup=keyboard,
    )
    await state.clear()


@router.message(F.text, StateFilter(FSMUserInputName.fullname))
async def process_incorrect_input_name(message: Message) -> None:
    """Обработка некорректного ввода имени и фамилии."""
    await message.answer(
        text=(
            "Некорректный ввод!\n"
            "Ваше сообщение должно содержать"
            "имя и фамилию, разделенные пробелом."
            "\n\nПопробуйте еще раз"
        )
    )


# ?============================================================================
# *========== ПРОЦЕСС ПРОХОЖДЕНИЯ ТЕСТА =======================================
# ?============================================================================
