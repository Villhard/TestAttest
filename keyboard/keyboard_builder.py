"""
Модуль для создания клавиатур.

Содержит функции для создания клавиатур для бота.

Функции:
    create_main_menu_keyboard:
        Создание главного меню.
    create_tests_menu_keyboard:
        Создание клавиатуры для списка тестов.
    create_test_menu_keyboard:
        Создание клавиатуры для меню теста.
    create_choice_answer_keyboard:
        Создание клавиатуры для выбора правильного ответа.
    create_confirm_keyboard:
        Создание клавиатуры для подтверждения действия.
    create_after_test_keyboard:
        Создание клавиатуры после прохождения теста.
    create_users_menu_keyboard:
        Создание клавиатуры для выбора пользователя.
    create_user_menu_keyboard:
        Создание клавиатуры просмотра пользователя.
    create_question_menu_keyboard:
        Создание клавиатуры для редактирования вопроса.
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.database import Question, Test, User, Answer
from database.admin_connect import get_test_id_by_question_id


def create_main_menu_keyboard(is_admin: bool) -> InlineKeyboardMarkup:
    """Создание главного меню."""
    # TODO: Добавлять меню по мере добавления новых функций
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(
        InlineKeyboardButton(text="Тесты", callback_data="tests")
    )
    if is_admin:
        keyboard_builder.row(
            InlineKeyboardButton(text="Пользователи", callback_data="users")
        )
    return keyboard_builder.as_markup()


def create_tests_menu_keyboard(
    tests: list[Test], is_admin: bool
) -> InlineKeyboardMarkup:
    """Создание клавиатуры."""
    keyboard_builder = InlineKeyboardBuilder()
    for button in tests:
        keyboard_builder.row(
            InlineKeyboardButton(
                text=(
                    f"{'🔒' if button.is_publish else '✏️'}" f" {button.title}"
                    if is_admin
                    else f"{button.title}"
                ),
                callback_data=f"test_{button.id}",
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


def create_test_menu_keyboard(
    test: Test,
    questions: list[Question],
    is_publish: bool,
) -> InlineKeyboardMarkup:
    """Создание клавиатуры для меню теста."""
    keyboard_builder = InlineKeyboardBuilder()
    if not is_publish:
        for button in questions:
            keyboard_builder.row(
                InlineKeyboardButton(
                    text=(f"{'🖼' if button.image else ''}" f" {button.text}"),
                    callback_data=f"question_{button.id}",
                )
            )
        keyboard_builder.row(
            InlineKeyboardButton(
                text="Добавить вопрос",
                callback_data=f"add_question_test_{test.id}",
            )
        )
        keyboard_builder.row(
            InlineKeyboardButton(
                text="Опубликовать тест",
                callback_data=f"confirm_publish_test_{test.id}",
            )
        )
    keyboard_builder.row(
        InlineKeyboardButton(
            text="Удалить тест", callback_data=f"confirm_delete_test_{test.id}"
        )
    )
    keyboard_builder.row(
        InlineKeyboardButton(text="Назад", callback_data="tests")
    )
    return keyboard_builder.as_markup()


def create_choice_answer_keyboard(
    answers: list[str] | dict[str, bool],
) -> InlineKeyboardMarkup:
    """Создание клавиатуры для выбора правильного ответа."""
    keyboard_builder = InlineKeyboardBuilder()
    for button in answers:
        keyboard_builder.row(
            InlineKeyboardButton(text=f"{button}", callback_data=f"{button}")
        )
    return keyboard_builder.as_markup()


def create_confirm_keyboard(
    callback_yes: str = "yes",
    callback_no: str = "no",
    text_yes: str = "Да",
    text_no: str = "Нет",
) -> InlineKeyboardMarkup:
    """Создание клавиатуры для подтверждения действия."""
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(
        InlineKeyboardButton(text=text_yes, callback_data=callback_yes),
        InlineKeyboardButton(text=text_no, callback_data=callback_no),
    )
    return keyboard_builder.as_markup()


def create_after_test_keyboard() -> InlineKeyboardMarkup:
    """Создание клавиатуры после прохождения теста."""
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(
        InlineKeyboardButton(text="Главное меню", callback_data="main_menu"),
    )
    return keyboard_builder.as_markup()


def create_users_menu_keyboard(users: list[User]) -> InlineKeyboardMarkup:
    """Создание клавиатуры для выбора пользователя."""
    keyboard_builder = InlineKeyboardBuilder()
    for button in users:
        keyboard_builder.row(
            InlineKeyboardButton(
                text=f"{button.name} {button.surname}",
                callback_data=f"user_{button.id}",
            )
        )
    keyboard_builder.row(
        InlineKeyboardButton(text="Назад", callback_data="main_menu")
    )
    return keyboard_builder.as_markup()


def create_user_menu_keyboard() -> InlineKeyboardMarkup:
    """Создание клавиатуры просмотра пользователя."""
    keyboard_builder = InlineKeyboardBuilder()  # TODO: Добавить функционал
    keyboard_builder.row(
        InlineKeyboardButton(text="Назад", callback_data="users")
    )
    return keyboard_builder.as_markup()


def create_question_menu_keyboard(
    answers: list[Answer],
) -> InlineKeyboardMarkup:
    """Создание клавиатуры для редактирования вопроса."""
    keyboard_builder = InlineKeyboardBuilder()
    for button in answers:
        keyboard_builder.row(
            InlineKeyboardButton(
                text=f"{'✅' if button.is_correct else ''} {button.text}",
                callback_data=(
                    f"edit_correct_answer_{button.question_id}_{button.id}"
                ),
            )
        )
    keyboard_builder.row(
        InlineKeyboardButton(
            text="Редактировать вопрос",
            callback_data=f"edit_question_{answers[0].question_id}",
        ),
    )
    keyboard_builder.row(
        InlineKeyboardButton(
            text="Удалить вопрос",
            callback_data=f"delete_question_{answers[0].question_id}",
        ),
    )
    keyboard_builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=(
                f"test_{get_test_id_by_question_id(answers[0].question_id)}"
            ),
        )
    )
    return keyboard_builder.as_markup()
