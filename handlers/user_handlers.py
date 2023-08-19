"""User handlers."""
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Command /start handler for user."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Список тестов", callback_data="tests")]]
    )
    await message.answer(
        text="Привет! Я бот для тестирования.\n\n"
        "Нажми на кнопку ниже, чтобы увидеть список доступный тестов.",
        reply_markup=keyboard,
    )


@router.callback_query(F.data == "tests")
async def cb_tests(callback: CallbackQuery) -> None:
    """Callback handler for tests for user."""
    #  TODO: get tests from database
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Тест 1", callback_data="test_1")],
            [InlineKeyboardButton(text="Тест 2", callback_data="test_2")],
        ]
    )
    await callback.message.edit_text(
        text="Выбери тест, который хочешь пройти.", reply_markup=keyboard
    )
