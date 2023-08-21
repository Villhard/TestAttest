"""Admin handlers."""
from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from config import config

router = Router()

router.message.filter(F.from_user.id.in_(config.bot.admin_ids))


class FSMCreateTest(StatesGroup):
    """Класс состояния создания теста."""

    title = State()
    description = State()
    count_questions = State()

    class FSMCreateQuestions(StatesGroup):
        """Класс состояния создания вопросов."""

        text = State()
        image = State()

        class FSMCreateAnswers(StatesGroup):
            """Класс состояния создания ответов."""

            text = State()
            is_correct = State()


@router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message) -> None:
    """Обработчик команды /start."""
    await message.answer("Привет, админ!")


@router.message(Command(commands=["create_test"]), StateFilter(default_state))
async def cmd_create_test(message: Message, state: FSMContext) -> None:
    """Обработчик команды /create_test."""
    await message.answer(text="Введите название теста")
    await state.set_state(FSMCreateTest.title)


@router.message(F.text, StateFilter(FSMCreateTest.title))
async def process_input_title(message: Message, state: FSMContext) -> None:
    """Обработчик ввода названия теста."""
    await state.update_data(title=message.text)
    await message.answer(text="Введите описание теста")
    await state.set_state(FSMCreateTest.description)


@router.message(F.text, StateFilter(FSMCreateTest.description))
async def process_input_description(message: Message, state: FSMContext) -> None:
    """Обработчик ввода описания теста."""
    await state.update_data(description=message.text)
    await message.answer(text="Введите количество вопросов в тесте")
    await state.set_state(FSMCreateTest.count_questions)


@router.message(F.text, StateFilter(FSMCreateTest.count_questions, lambda msg: msg.text.isdigit()))
async def process_input_count_questions(message: Message, state: FSMContext) -> None:
    """Обработчик ввода количества вопросов в тесте."""
    await state.update_data(count_questions=int(message.text))
    data = await state.get_data()  # FIXME # ! убрать проверку получения данных
    await message.answer(text=f"Тест: {data['title']}\nОписание: {data['description']}")
    await state.clear()

    # TODO: Создание вопросов и ответов
