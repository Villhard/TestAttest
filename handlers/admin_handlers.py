"""Admin handlers."""
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
    Message,
    PhotoSize,
)

from config import config
from database import admin_connect
from keyboard import keyboard_builder
from utils import admin_utils

router = Router()

router.message.filter(F.from_user.id.in_(config.bot.admin_ids))


# ?============================================================================
# *========== МАШИНЫ СОСТОЯНИЙ ================================================
# ?============================================================================


class FSMCreateTest(StatesGroup):
    """Класс состояния создания теста."""

    title = State()
    description = State()
    image = State()


class FSMCreateQuestions(StatesGroup):
    """Класс состояния создания вопросов."""

    text = State()
    answers = State()
    image = State()


# ?============================================================================
# *========== НАВИГАЦИЯ =======================================================
# ?============================================================================


@router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message) -> None:
    """Приветствие админа."""
    keyboard = keyboard_builder.create_main_menu_keyboard(
        is_admin=True,
    )
    await message.answer(
        text="Привет, админ!",
        reply_markup=keyboard,
    )


@router.message(Command(commands="help"), StateFilter(default_state))
async def cmd_help(message: Message) -> None:
    """Помощь админу."""
    pass


@router.callback_query(F.data == "main_menu", StateFilter(default_state))
async def call_main_menu(callback: CallbackQuery) -> None:
    """Главное меню."""
    keyboard = keyboard_builder.create_main_menu_keyboard(
        is_admin=True,
    )
    await callback.message.edit_text(
        text="Главное меню",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(F.data == "tests", StateFilter(default_state))
async def call_tests(callback: CallbackQuery) -> None:
    """Просмотр всех тестов."""
    keyboard = keyboard_builder.create_tests_keyboard(
        tests=admin_connect.get_tests(),
        is_admin=True,
    )
    await callback.message.edit_text(
        text="Список тестов", reply_markup=keyboard
    )
    await callback.answer()


@router.callback_query(
    lambda call: re.fullmatch(r"test_\d+", call.data),
    StateFilter(default_state),
)
async def call_test_with_id(callback: CallbackQuery) -> None:
    """Просмотр теста."""
    test_id = int(callback.data.split("_")[1])
    test = admin_connect.get_test_by_id(test_id)
    is_publish = test.is_publish
    keyboard = keyboard_builder.create_test_keyboard(
        test=test,
        questions=admin_connect.get_questions_by_test_id(test_id),
        is_publish=is_publish,
    )
    if is_publish:
        await callback.message.edit_text(
            text=(
                f"<b>{test.title}</b>\n{test.description}"
                "\n\n<b>Cтатистика:</b>\n"
                "В процессе разработки"  # TODO: Добавить статистику
            ),
            reply_markup=keyboard,
        )
    else:
        await callback.message.edit_text(
            text=f"<b>{test.title}</b>\n{test.description}",
            reply_markup=keyboard,
        )
    await callback.answer()


# ?============================================================================
# *========== СОЗДАНИЕ, РЕДАКТИРОВАНИЕ И УДАЛЕНИЕ ТЕСТА И ВОПРОСОВ ============
# ?============================================================================


@router.callback_query(F.data == "add_test", StateFilter(default_state))
async def call_add_test(callback: CallbackQuery, state: FSMContext) -> None:
    """Создание теста."""
    await callback.message.edit_text(text="Введите название теста")
    await callback.answer()
    await state.set_state(FSMCreateTest.title)


@router.callback_query(
    lambda call: re.fullmatch(r"confirm_delete_test_\d+", call.data),
    StateFilter(default_state),
)
async def call_confirm_delete_test(callback: CallbackQuery) -> None:
    """Подтверждение удаления теста."""
    test_id = int(callback.data.split("_")[3])
    keyboard = keyboard_builder.create_confirm_keyboard(
        callback_yes=f"delete_test_{test_id}",
        callback_no=f"test_{test_id}",
    )
    await callback.message.edit_text(
        text="Вы уверены, что хотите удалить тест?",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(
    lambda call: re.fullmatch(r"delete_test_\d+", call.data),
    StateFilter(default_state),
)
async def call_delete_test(callback: CallbackQuery) -> None:
    """Удаление теста."""
    test_id = int(callback.data.split("_")[2])
    admin_utils.delete_test_dir(test_id)
    admin_connect.delete_test_by_id(test_id)
    keyboard = keyboard_builder.create_tests_keyboard(
        tests=admin_connect.get_tests(),
        is_admin=True,
    )
    await callback.message.edit_text(
        text="Тест успешно удален!", reply_markup=keyboard
    )
    await callback.answer()


@router.callback_query(
    lambda call: re.fullmatch(r"publish_test_\d+", call.data),
    StateFilter(default_state),
)
async def call_publish_test(callback: CallbackQuery) -> None:
    """Публикация теста."""
    test_id = int(callback.data.split("_")[2])
    admin_connect.publish_test_by_id(test_id)
    keyboard = keyboard_builder.create_tests_keyboard(
        tests=admin_connect.get_tests(),
        is_admin=True,
    )
    await callback.message.edit_text(
        text="Тест успешно опубликован!", reply_markup=keyboard
    )
    await callback.answer()


# ?============================================================================
# *========== ПРОЦЕСС СОЗДАНИЯ ТЕСТА ==========================================
# ?============================================================================


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
    admin_connect.create_test(test["title"], test["description"])
    admin_utils.create_test_dir(admin_connect.get_tests()[-1].id)
    keyboard = keyboard_builder.create_tests_keyboard(
        tests=admin_connect.get_tests(),
        is_admin=True,
    )
    await message.answer(text="Тест успешно создан!", reply_markup=keyboard)
    await state.clear()
    await state.set_state(default_state)


# ?============================================================================
# *========== ПРОЦЕСС СОЗДАНИЯ ВОПРОСА ========================================
# ?============================================================================


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
        keyboard = keyboard_builder.create_answers_keyboard(answers)
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
    number_image = admin_utils.get_next_number_image(test_id)
    await message.bot.download(
        photo_path,
        destination=f"img/test_{test_id}/question_{number_image}.jpg",
    )
    admin_connect.create_question(
        test_id=test_id,
        text=question,
        answers=answers,
        image=f"question_{number_image}.jpg",
    )
    test = admin_connect.get_test_by_id(test_id)
    keyboard = keyboard_builder.create_test_keyboard(
        test=test,
        questions=admin_connect.get_questions_by_test_id(test_id),
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
    admin_connect.create_question(
        test_id=test_id,
        text=question,
        answers=answers,
        image=None,
    )
    test = admin_connect.get_test_by_id(test_id)
    keyboard = keyboard_builder.create_test_keyboard(
        test=test,
        questions=admin_connect.get_questions_by_test_id(test_id),
        is_publish=test.is_publish,
    )
    await callback.message.edit_text(
        text="Вопрос успешно создан!",
        reply_markup=keyboard,
    )
    await state.clear()
    await state.set_state(default_state)
