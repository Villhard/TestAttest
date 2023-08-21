"""Admin handlers."""
import re
from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from config import config
from database import admin_connect
from keyboard.keyboard_builder import (
    create_edit_test_keyboard,
    create_main_menu_keyboard,
    create_tests_keyboard,
)

router = Router()

router.message.filter(F.from_user.id.in_(config.bot.admin_ids))


class FSMCreateTest(StatesGroup):
    """Класс состояния создания теста."""

    title = State()
    description = State()


class FSMCreateQuestions(StatesGroup):
    """Класс состояния создания вопросов."""

    text = State()
    image = State()
    answer_1 = State()
    answer_2 = State()
    answer_3 = State()
    answer_4 = State()
    correct_answer = State()


@router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message) -> None:
    """Приветствие админа."""
    keyboard = create_main_menu_keyboard(message.from_user.id in config.bot.admin_ids)
    await message.answer(
        "Привет, админ!",
        reply_markup=keyboard,
    )


@router.message(Command(commands="help"), StateFilter(default_state))
async def cmd_help(message: Message) -> None:
    """Помощь админу."""
    pass


@router.callback_query(F.data == "main_menu", StateFilter(default_state))
async def call_main_menu(callback: CallbackQuery) -> None:
    """Главное меню."""
    keyboard = create_main_menu_keyboard(callback.from_user.id in config.bot.admin_ids)
    await callback.message.edit_text(text="Главное меню", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "tests", StateFilter(default_state))
async def call_tests(callback: CallbackQuery) -> None:
    """Просмотр всех тестов."""
    tests = admin_connect.get_tests()
    keyboard = create_tests_keyboard(tests, callback.from_user.id in config.bot.admin_ids)
    await callback.message.edit_text(text="Список тестов", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(
    lambda call: re.fullmatch(r"test_\d+_False", call.data),
    StateFilter(default_state),
)
async def call_test_with_id(callback: CallbackQuery) -> None:
    """Редактирование теста."""
    test_id = int(callback.data.split("_")[1])
    test = admin_connect.get_test_by_id(test_id)
    questions = admin_connect.get_questions_by_test_id(test_id)
    keyboard = create_edit_test_keyboard(test, questions)
    await callback.message.edit_text(
        text=f"<b>{test.title}</b>\n{test.description}",
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
    keyboard = create_main_menu_keyboard(callback.from_user.id in config.bot.admin_ids)
    admin_connect.delete_test_by_id(test_id)
    await callback.message.edit_text(text="Тест успешно удален!", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "add_test", StateFilter(default_state))
async def call_add_test(callback: CallbackQuery, state: FSMContext) -> None:
    """Создание теста."""
    await callback.message.edit_text(text="Введите название теста")
    await callback.answer()
    await state.set_state(FSMCreateTest.title)


@router.message(F.text, StateFilter(FSMCreateTest.title))
async def process_input_title(message: Message, state: FSMContext) -> None:
    """Создание теста. Получение названия теста."""
    await state.update_data(title=message.text)
    await message.answer(text="Введите описание теста")
    await state.set_state(FSMCreateTest.description)


@router.message(F.text, StateFilter(FSMCreateTest.description))
async def process_input_description(message: Message, state: FSMContext) -> None:
    """Создание теста. Получение описания теста."""
    await state.update_data(description=message.text)
    test = await state.get_data()
    keyboard = create_main_menu_keyboard(message.from_user.id in config.bot.admin_ids)
    admin_connect.create_test(test["title"], test["description"])
    await message.answer(text="Тест успешно создан!",
                         reply_markup=keyboard)
    await state.clear()
    await state.set_state(default_state)


# TODO: Создание вопросов и ответов
