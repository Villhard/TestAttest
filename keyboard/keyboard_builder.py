"""Модуль для создания клавиатур."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.database import Question, Test


def create_main_menu_keyboard(is_admin: bool) -> InlineKeyboardMarkup:
    """Создание главного меню."""
    # TODO: Добавлять меню по мере добавления новых функций
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(
        InlineKeyboardButton(text="Тесты", callback_data="tests")
    )
    return keyboard_builder.as_markup()


def create_tests_keyboard(
    tests: list[Test], is_admin: bool
) -> InlineKeyboardMarkup:
    """Создание клавиатуры."""
    keyboard_builder = InlineKeyboardBuilder()
    for button in tests:
        keyboard_builder.row(
            InlineKeyboardButton(
                text=f"{'🔒' if button.is_publish else '✏️'}"
                f" {button.title}",
                callback_data=f"test_{button.id}_{button.is_publish}",
            )
        )
    if is_admin:
        keyboard_builder.row(
            InlineKeyboardButton(
                text="Добавить тест", callback_data="add_test"
            )
        )
    keyboard_builder.row(
        InlineKeyboardButton(text="Назад", callback_data="main_menu")
    )
    return keyboard_builder.as_markup()


def create_test_keyboard(
    test: Test,
    questions: list[Question],
    is_publish: bool,
    is_exists_image: bool,
) -> InlineKeyboardMarkup:
    """Создание клавиатуры для меню теста."""
    keyboard_builder = InlineKeyboardBuilder()
    if is_exists_image:
        if not is_publish:
            for button in questions:
                keyboard_builder.row(
                    InlineKeyboardButton(
                        text=f"{button.text}",
                        callback_data=f"question_{button.id}",
                    )
                )
            # TODO: Добавить функцию добавления вопроса
            keyboard_builder.row(
                InlineKeyboardButton(
                    text="Добавить вопрос",
                    callback_data=f"add_question_test_{test.id}",
                )
            )
            keyboard_builder.row(
                InlineKeyboardButton(
                    text="Опубликовать тест",
                    callback_data=f"publish_test_{test.id}",
                )
            )
    else:
        keyboard_builder.row(
            InlineKeyboardButton(
                text="Добавить изображение теста",
                callback_data=f"add_image_test_{test.id}",
            )
        )
    keyboard_builder.row(
        InlineKeyboardButton(
            text="Удалить тест", callback_data=f"delete_test_{test.id}"
        )
    )
    keyboard_builder.row(
        InlineKeyboardButton(text="Назад", callback_data="tests")
    )
    return keyboard_builder.as_markup()
