# todo: Добавить пагинацию для клавиатур со списками.
from random import shuffle

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import config, lexicon
from database.database import Question, Test, User, Answer
from database.admin_connect import (
    get_test_id_by_question_id,
    get_count_results_by_user_id,
    get_results_by_user_id,
    get_test_by_id,
)


def create_main_menu_keyboard(
    is_admin: bool = False,
) -> InlineKeyboardMarkup:
    """Create main menu keyboard."""
    # todo: Добавлять меню по мере добавления новых функций
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(
        InlineKeyboardButton(
            text=lexicon.BUTTONS['tests'], callback_data="tests"
        )
    )
    if is_admin:
        keyboard_builder.row(
            InlineKeyboardButton(
                text=lexicon.BUTTONS['users'], callback_data="users"
            )
        )
    return keyboard_builder.as_markup()


def create_tests_menu_keyboard(
    tests: list[Test],
    is_admin: bool = False,
) -> InlineKeyboardMarkup:
    """Create tests menu keyboard."""
    keyboard_builder = InlineKeyboardBuilder()
    for test in tests:
        keyboard_builder.row(
            InlineKeyboardButton(
                text=(
                    f"{'🟢' if test.is_publish else '🔴'} {test.title}"
                    if is_admin
                    else f"{test.title}"
                ),
                callback_data=f"test {test.id}",
            )
        )
    if is_admin:
        keyboard_builder.row(
            InlineKeyboardButton(
                text=lexicon.BUTTONS['add test'], callback_data="add test"
            )
        )
    keyboard_builder.row(
        InlineKeyboardButton(
            text=lexicon.BUTTONS['back'], callback_data="main menu"
        )
    )
    return keyboard_builder.as_markup()


def create_test_menu_keyboard(
    test: Test,
    questions: list[Question],
    is_publish: bool,
) -> InlineKeyboardMarkup:
    """Create test menu keyboard."""
    keyboard_builder = InlineKeyboardBuilder()
    if not is_publish:
        keyboard_builder.row(
            InlineKeyboardButton(
                text=lexicon.BUTTONS["view questions"].format(
                    count=len(questions) if questions else 0
                ),
                # todo: создать хендлер для получения вопросов
                callback_data="test_questions",
            )
        )
        keyboard_builder.row(
            InlineKeyboardButton(
                text=lexicon.BUTTONS["add question"],
                callback_data=f"add_question_test_{test.id}",
            )
        )
        keyboard_builder.row(
            InlineKeyboardButton(
                text=lexicon.BUTTONS["publish test"],
                callback_data=f"confirm_publish_test_{test.id}",
            )
        )
    keyboard_builder.row(
        InlineKeyboardButton(
            text=lexicon.BUTTONS["delete test"],
            callback_data=f"confirm_delete_test_{test.id}"
        )
    )
    keyboard_builder.row(
        InlineKeyboardButton(text=lexicon.BUTTONS["back"], callback_data="tests")
    )
    return keyboard_builder.as_markup()


def create_choice_answer_keyboard(
    answers: list[str],
) -> InlineKeyboardMarkup:
    """Create choice answer keyboard."""
    keyboard_builder = InlineKeyboardBuilder()

    for answer in answers:
        keyboard_builder.row(
            InlineKeyboardButton(text=f"{answer}", callback_data=f"{answer}")
        )
    return keyboard_builder.as_markup()


def create_test_answers_keyboard(
    answers: list[Answer],
) -> InlineKeyboardMarkup:
    """Create test answers keyboard."""
    keyboard_builder = InlineKeyboardBuilder()

    shuffle(answers)
    for answer in answers:
        keyboard_builder.row(
            InlineKeyboardButton(
                text=f"{answer.text}", callback_data=f"{answer.id}"
            )
        )
    return keyboard_builder.as_markup()


def create_confirm_keyboard(
    callback_yes: str = "yes",
    callback_no: str = "no",
    text_yes: str = lexicon.BUTTONS['yes'],
    text_no: str = lexicon.BUTTONS['no'],
) -> InlineKeyboardMarkup:
    """Create confirm keyboard."""
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(
        InlineKeyboardButton(text=text_yes, callback_data=callback_yes),
        InlineKeyboardButton(text=text_no, callback_data=callback_no),
    )
    return keyboard_builder.as_markup()


def create_after_test_keyboard() -> InlineKeyboardMarkup:
    """Create after test keyboard."""
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(
        InlineKeyboardButton(text=lexicon.BUTTONS['main menu'], callback_data="main_menu"),
    )
    return keyboard_builder.as_markup()


def create_users_menu_keyboard(users: list[User]) -> InlineKeyboardMarkup:
    """Create users menu keyboard."""
    keyboard_builder = InlineKeyboardBuilder()
    for user in users:
        result = get_count_results_by_user_id(user.id)
        keyboard_builder.row(
            InlineKeyboardButton(
                text=(
                    f"{user.name} {user.surname}"
                    f" {result['completed']}/{result['total']}"
                ),
                callback_data=f"user {user.id}",
            )
        )
    keyboard_builder.row(
        InlineKeyboardButton(
            text=lexicon.BUTTONS['back'], callback_data="main menu"
        )
    )
    return keyboard_builder.as_markup()


def create_user_menu_keyboard(
    user: User,
) -> InlineKeyboardMarkup:
    """Create user menu keyboard."""
    keyboard_builder = InlineKeyboardBuilder()  # todo: Добавить функционал
    results = get_results_by_user_id(user_id=user.id)
    for result in results:
        test = get_test_by_id(result.test_id)
        keyboard_builder.row(
            InlineKeyboardButton(
                text=(
                    f"{'✅' if result.score >= config.pass_score else '❌'}"
                    f" {test.title} - {result.score}"
                ),
                callback_data=f"result_{result.id}",
            )
        )
    keyboard_builder.row(
        InlineKeyboardButton(text=lexicon.BUTTONS['back'], callback_data="users")
    )
    return keyboard_builder.as_markup()


def create_question_menu_keyboard(
    answers: list[Answer],
) -> InlineKeyboardMarkup:
    """Create question menu keyboard."""
    keyboard_builder = InlineKeyboardBuilder()
    for answer in answers:
        keyboard_builder.row(
            InlineKeyboardButton(
                text=f"{'✅' if answer.is_correct else ''} {answer.text}",
                callback_data=(
                    f"edit_correct_answer_{answer.question_id}_{answer.id}"
                ),
            )
        )
    keyboard_builder.row(
        InlineKeyboardButton(
            text=lexicon.BUTTONS['edit question'],
            callback_data=f"edit_question_{answers[0].question_id}",
        ),
    )
    keyboard_builder.row(
        InlineKeyboardButton(
            text=lexicon.BUTTONS['delete question'],
            callback_data=f"delete_question_{answers[0].question_id}",
        ),
    )
    keyboard_builder.row(
        InlineKeyboardButton(
            text=lexicon.BUTTONS['back'],
            callback_data=(
                f"test_{get_test_id_by_question_id(answers[0].question_id)}"
            ),
        )
    )
    return keyboard_builder.as_markup()


def create_back_button_keyboard(
    callback_data: str,
    mgs: str = lexicon.BUTTONS['back'],
) -> InlineKeyboardMarkup:
    """Create back button keyboard."""
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(
        InlineKeyboardButton(text=mgs, callback_data=callback_data)
    )
    return keyboard_builder.as_markup()
