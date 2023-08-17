from aiogram import Router, F
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery,
)
from aiogram.filters import CommandStart


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """/start command handler"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Список тестов", callback_data="tests")]
        ]
    )
    await message.answer(
        text="Привет! Я бот для тестирования.\n\n"
        "Нажми на кнопку ниже, чтобы увидеть список доступный тестов.",
        reply_markup=keyboard,
    )


@router.callback_query(F.data == "tests")
async def cb_tests(callback: CallbackQuery):
    """Tests callback handler"""
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
