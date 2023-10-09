"""
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
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    PhotoSize,
)

from config import config
from database import admin_connect as db
from handlers.admin_handlers.states import FSMCreateTest, FSMCreateQuestions
from keyboard import keyboard_builder as kb
from utils import admin_utils as utils

router = Router()

router.callback_query.filter(F.from_user.id.in_(config.bot.admin_ids))
router.message.filter(F.from_user.id.in_(config.bot.admin_ids))


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
