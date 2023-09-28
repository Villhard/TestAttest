"""
Admin handlers.

Машины состояний:
    FSMCreateTest:
        title - ввод названия теста
        description - ввод описания теста
    FSMCreateQuestions:
        text - ввод текста вопроса
        answers - ввод текста ответов
        image - ввод изображения вопроса

Навигация:
    cmd_start:
        Приветствие админа
    cmd_help:
        Помощь админу
    call_main_menu:
        Главное меню
    call_tests:
        Просмотр всех тестов
    call_test_by_id:
        Просмотр теста
    call_question_by_id:
        Просмотр вопроса
    call_users:
        Просмотр пользователей
    call_user_by_id:
        Просмотр пользователя
    call_result_by_id:
        Просмотр результата

Создание, редактирование и удаление теста и вопросов:
    call_add_test:
        Создание теста
    call_confirm_delete_test:
        Подтверждение удаления теста
    call_delete_test:
        Удаление теста
    call_confirm_publish_test:
        Подтверждение публикации теста
    call_publish_test:
        Публикация теста
    call_edit_correct_answer:
        Редактирование правильного ответа
    call_delete_question:
        Удаление вопроса

Процесс создания теста:
    process_input_title:
        Создание теста. Получение названия теста
    process_input_description:
        Создание теста. Получение описания теста

Процесс создания вопроса:
    call_add_question:
        Создание вопроса
    process_input_question_text:
        Создание вопроса. Получение текста вопроса
    process_input_answers_text:
        Создание вопроса. Получение текста ответов
    process_input_correct_answer:
        Создание вопроса. Получение правильного ответа
    process_input_image_question:
        Создание вопроса. Получение изображения вопроса
    process_skip_image_question:
        Создание вопроса. Пропуск изображения вопроса
"""
import re

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    PhotoSize,
)
from loguru import logger

from config import config
from database import admin_connect as db
from keyboard import keyboard_builder as kb
from utils import admin_utils as utils

router = Router()

router.callback_query.filter(F.from_user.id.in_(config.bot.admin_ids))
router.message.filter(F.from_user.id.in_(config.bot.admin_ids))


# =============================================================================
# =========== МАШИНЫ СОСТОЯНИЙ ================================================
# =============================================================================


class FSMCreateTest(StatesGroup):
    """
    Класс состояния создания теста.

    title:
        Ввод названия теста
    description:
        Ввод описания теста
    """

    title = State()
    description = State()


class FSMCreateQuestions(StatesGroup):
    """
    Класс состояния создания вопросов.

    text:
        Ввод текста вопроса
    answers:
        Ввод текста ответов
    image:
        Ввод изображения вопроса
    """

    text = State()
    answers = State()
    image = State()


# =============================================================================
# =========== НАВИГАЦИЯ =======================================================
# =============================================================================


@router.callback_query(F.data == "tests", StateFilter(default_state))
async def call_tests(callback: CallbackQuery) -> None:
    """Просмотр всех тестов."""
    tests = db.get_tests()
    keyboard = kb.create_tests_menu_keyboard(
        tests=tests,
        is_admin=True,
    )
    await callback.message.edit_text(
        text="Список тестов", reply_markup=keyboard
    )


@router.callback_query(
    lambda call: re.fullmatch(r"test_\d+", call.data),
    StateFilter(default_state),
)
async def call_test_by_id(callback: CallbackQuery) -> None:
    """Просмотр теста."""
    test_id = int(callback.data.split("_")[1])
    test = db.get_test_by_id(test_id)
    questions = db.get_questions_by_test_id(test_id)
    keyboard = kb.create_test_menu_keyboard(
        test=test,
        questions=questions,
        is_publish=test.is_publish,
    )

    text = f"<b>{test.title}</b>\n{test.description}"

    if test.is_publish:
        statistics = db.get_statistics_by_test_id(test_id)
        text += (
            f"\n\n<b>Статистика:</b>\n"
            "Успех/Всего: "
            f"{statistics['completed']}/{statistics['total']}"
        )

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
    )


@router.callback_query(
    lambda call: re.fullmatch(r"question_\d+", call.data),
    StateFilter(default_state),
)
async def call_question_by_id(callback: CallbackQuery) -> None:
    """Просмотр вопроса."""
    question_id = int(callback.data.split("_")[1])
    question, answers = db.get_question_by_id(question_id)
    keyboard = kb.create_question_menu_keyboard(
        answers=answers,
    )

    await callback.message.edit_text(
        text=question.text,
        reply_markup=keyboard,
    )


@router.callback_query(
    F.data == "users",
    StateFilter(default_state),
)
async def call_users(callback: CallbackQuery) -> None:
    """Просмотр пользователей."""
    users = db.get_users()
    keyboard = kb.create_users_menu_keyboard(users)

    await callback.message.edit_text(
        text="Все пользователи",
        reply_markup=keyboard,
    )


@router.callback_query(
    lambda call: re.fullmatch(r"user_\d+", call.data),
    StateFilter(default_state),
)
async def call_user_by_id(callback: CallbackQuery) -> None:
    """Просмотр пользователя."""
    user_id = int(callback.data.split("_")[1])
    user = db.get_user_by_id(user_id)
    results = db.get_count_results_by_user_id(user_id)
    keyboard = kb.create_user_menu_keyboard(user)

    await callback.message.edit_text(
        text=(
            f"<b>{user.name} {user.surname}</b>\n\n"
            f"Тестов пройдено: {results['completed']}/{results['total']}"
        ),
        reply_markup=keyboard,
    )


@router.callback_query(
    lambda call: re.fullmatch(r"result_\d+", call.data),
    StateFilter(default_state),
)
async def call_result_by_id(callback: CallbackQuery) -> None:
    """Просмотр результата."""
    result_id = int(callback.data.split("_")[1])
    result = db.get_result_by_id(result_id)
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

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
    )


# =============================================================================
# =========== СОЗДАНИЕ, РЕДАКТИРОВАНИЕ И УДАЛЕНИЕ ТЕСТА И ВОПРОСОВ ============
# =============================================================================


@router.callback_query(F.data == "add_test", StateFilter(default_state))
async def call_add_test(callback: CallbackQuery, state: FSMContext) -> None:
    """Создание теста."""
    await callback.message.edit_text(text="Введите название теста")
    await state.set_state(FSMCreateTest.title)


@router.callback_query(
    lambda call: re.fullmatch(r"confirm_delete_test_\d+", call.data),
    StateFilter(default_state),
)
async def call_confirm_delete_test(callback: CallbackQuery) -> None:
    """Подтверждение удаления теста."""
    test_id = int(callback.data.split("_")[3])
    keyboard = kb.create_confirm_keyboard(
        callback_yes=f"delete_test_{test_id}",
        callback_no=f"test_{test_id}",
    )

    await callback.message.edit_text(
        text="Вы уверены, что хотите удалить тест?",
        reply_markup=keyboard,
    )


@router.callback_query(
    lambda call: re.fullmatch(r"delete_test_\d+", call.data),
    StateFilter(default_state),
)
async def call_delete_test(callback: CallbackQuery) -> None:
    """Удаление теста."""
    test_id = int(callback.data.split("_")[2])
    utils.delete_test_dir(test_id)
    db.delete_test_by_id(test_id)
    keyboard = kb.create_tests_menu_keyboard(
        tests=db.get_tests(),
        is_admin=True,
    )

    await callback.message.edit_text(
        text="Тест успешно удален!", reply_markup=keyboard
    )


@router.callback_query(
    lambda call: re.fullmatch(r"confirm_publish_test_\d+", call.data),
    StateFilter(default_state),
)
async def call_confirm_publish_test(callback: CallbackQuery) -> None:
    """Подтверждение публикации теста."""
    test_id = int(callback.data.split("_")[3])
    keyboard = kb.create_confirm_keyboard(
        callback_yes=f"publish_test_{test_id}",
        callback_no=f"test_{test_id}",
    )

    await callback.message.edit_text(
        text="Вы уверены, что хотите опубликовать тест?",
        reply_markup=keyboard,
    )


@router.callback_query(
    lambda call: re.fullmatch(r"publish_test_\d+", call.data),
    StateFilter(default_state),
)
async def call_publish_test(callback: CallbackQuery) -> None:
    """Публикация теста."""
    test_id = int(callback.data.split("_")[2])
    db.publish_test_by_id(test_id)
    keyboard = kb.create_tests_menu_keyboard(
        tests=db.get_tests(),
        is_admin=True,
    )

    await callback.message.edit_text(
        text="Тест успешно опубликован!", reply_markup=keyboard
    )


@router.callback_query(
    lambda call: re.fullmatch(r"edit_correct_answer_\d+_\d+", call.data),
    StateFilter(default_state),
)
async def call_edit_correct_answer(callback: CallbackQuery) -> None:
    """Редактирование правильного ответа."""
    question_id = int(callback.data.split("_")[3])
    answer_id = int(callback.data.split("_")[4])
    db.change_correct_answer(question_id, answer_id)
    question, answers = db.get_question_by_id(question_id)
    keyboard = kb.create_question_menu_keyboard(
        answers=answers,
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
async def call_delete_question(callback: CallbackQuery) -> None:
    """Удаление вопроса."""
    question_id = int(callback.data.split("_")[2])
    test = db.get_test_by_question_id(question_id)
    db.delete_question_by_id(question_id)
    keyboard = kb.create_test_menu_keyboard(
        test=test,
        questions=db.get_questions_by_test_id(test.id),
        is_publish=test.is_publish,
    )

    await callback.answer(
        text="Вопрос успешно удален!",
    )
    await callback.message.edit_text(
        text=f"<b>{test.title}</b>\n{test.description}",
        reply_markup=keyboard,
    )


# =============================================================================
# =========== ПРОЦЕСС СОЗДАНИЯ ТЕСТА ==========================================
# =============================================================================


@router.message(F.text, StateFilter(FSMCreateTest.title))
async def process_input_title(message: Message, state: FSMContext) -> None:
    """Создание теста. Получение названия теста."""
    await state.update_data(title=message.text)
    await message.answer(text="Введите описание теста")
    await state.set_state(FSMCreateTest.description)


@router.message(F.text, StateFilter(FSMCreateTest.description))
async def process_input_description(
    message: Message, state: FSMContext
) -> None:
    """Создание теста. Получение описания теста."""
    await state.update_data(description=message.text)
    test = await state.get_data()
    db.create_test(test["title"], test["description"])
    utils.create_test_dir(db.get_tests()[0].id)
    keyboard = kb.create_tests_menu_keyboard(
        tests=db.get_tests(),
        is_admin=True,
    )
    await message.answer(text="Тест успешно создан!", reply_markup=keyboard)
    await state.clear()
    await state.set_state(default_state)


# =============================================================================
# =========== ПРОЦЕСС СОЗДАНИЯ ВОПРОСА ========================================
# =============================================================================


@router.callback_query(
    lambda call: re.fullmatch(r"add_question_test_\d+", call.data),
    StateFilter(default_state),
)
async def call_add_question(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """Создание вопроса."""
    await state.update_data(test_id=int(callback.data.split("_")[3]))
    await state.update_data(answers=[])  # Создание списка ответов
    await callback.message.edit_text(text="Введите текст вопроса")
    await state.set_state(FSMCreateQuestions.text)


@router.message(F.text, StateFilter(FSMCreateQuestions.text))
async def process_input_question_text(
    message: Message, state: FSMContext
) -> None:
    """Создание вопроса. Получение текста вопроса."""
    await state.update_data(text=message.text)
    await message.answer(text="Введите текст ответа №1")
    await state.set_state(FSMCreateQuestions.answers)


@router.message(F.text, StateFilter(FSMCreateQuestions.answers))
async def process_input_answers_text(
    message: Message, state: FSMContext
) -> None:
    """Создание вопроса. Получение текста ответов."""
    data = await state.get_data()
    answers = data["answers"]
    answers.append(message.text)
    await state.update_data(answers=answers)
    if len(answers) < 4:
        await message.answer(text=f"Введите текст ответа №{len(answers) + 1}")
    else:
        keyboard = kb.create_choice_answer_keyboard(answers)
        await message.answer(
            text="Выберите правильный ответ",
            reply_markup=keyboard,
        )


@router.callback_query(F.data, StateFilter(FSMCreateQuestions.answers))
async def process_input_correct_answer(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """Создание вопроса. Получение правильного ответа."""
    data = await state.get_data()
    await state.update_data(
        answers={
            answer: is_correct
            for answer in data["answers"]
            for is_correct in [True if answer == callback.data else False]
        }
    )
    await callback.message.edit_text(
        text="Отправьте изображение или нажмите пропустить",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Пропустить", callback_data="skip")]
            ]
        ),
    )
    await state.set_state(FSMCreateQuestions.image)


@router.message(F.photo, StateFilter(FSMCreateQuestions.image))
async def process_input_image_question(
    message: Message, state: FSMContext
) -> None:
    """Создание вопроса. Получение изображения вопроса."""
    data = await state.get_data()
    test_id = data["test_id"]
    question = data["text"]
    answers = data["answers"]
    photo: PhotoSize = message.photo[-1]
    photo_path = photo.file_id
    number_image = utils.get_next_number_image(test_id)
    await message.bot.download(
        photo_path,
        destination=f"img/test_{test_id}/img_{number_image}.jpg",
    )
    db.create_question(
        test_id=test_id,
        text=question,
        answers=answers,
        image=f"img_{number_image}.jpg",
    )
    test = db.get_test_by_id(test_id)
    keyboard = kb.create_test_menu_keyboard(
        test=test,
        questions=db.get_questions_by_test_id(test_id),
        is_publish=test.is_publish,
    )
    await message.answer(
        text="Вопрос успешно создан!",
        reply_markup=keyboard,
    )
    await state.clear()
    await state.set_state(default_state)


@router.callback_query(F.data == "skip", StateFilter(FSMCreateQuestions.image))
async def process_skip_image_question(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """Создание вопроса. Пропуск изображения вопроса."""
    data = await state.get_data()
    test_id = data["test_id"]
    question = data["text"]
    answers = data["answers"]
    db.create_question(
        test_id=test_id,
        text=question,
        answers=answers,
    )
    test = db.get_test_by_id(test_id)
    keyboard = kb.create_test_menu_keyboard(
        test=test,
        questions=db.get_questions_by_test_id(test_id),
        is_publish=test.is_publish,
    )
    await callback.message.edit_text(
        text="Вопрос успешно создан!",
        reply_markup=keyboard,
    )
    await state.clear()
    await state.set_state(default_state)
