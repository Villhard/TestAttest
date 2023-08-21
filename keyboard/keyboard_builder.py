"""Модуль для создания клавиатур."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.database import Test


def create_tests_keyboard(tests: list[Test], is_admin: bool) -> InlineKeyboardMarkup:
    """Создание клавиатуры."""
    keyboard_builder = InlineKeyboardBuilder()
    for button in tests:
        keyboard_builder.row(InlineKeyboardButton(text=button.title, callback_data=str(button.id)))
    if is_admin:
        keyboard_builder.row(InlineKeyboardButton(text="Добавить тест", callback_data="add_test"))
    keyboard_builder.row(InlineKeyboardButton(text="Назад", callback_data="back"))
    return keyboard_builder.as_markup()
