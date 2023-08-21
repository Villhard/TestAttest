"""User handlers."""
from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from database import user_connect

router = Router()


class FSMUserInputName(StatesGroup):
    """Класс состояния ввода имени пользователя."""

    fullname = State()


@router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message, state: FSMContext) -> None:
    """Приветствие пользователя или запрос имени и фамилии."""
    user = user_connect.check_user_exists(message.from_user.id)
    if user:
        await message.answer(text=f"Здравствуйте, {user.name}!")
    else:
        await message.answer(
            text=(
                "Добро пожаловать в бота для тестирования!"
                "\n\nВведите ваше имя и фалимию"
            )
        )
        await state.set_state(FSMUserInputName.fullname)


@router.message(
    F.text, StateFilter(FSMUserInputName.fullname), lambda msg: len(msg.text.split()) == 2
)
async def process_input_name(message: Message, state: FSMContext) -> None:
    """Получение имени и фамилии пользователя."""
    name, surname = message.text.title().split()
    user_connect.create_user(message.from_user.id, name, surname)
    await message.answer(text="Вы успешно зарегистрировались!")
    await state.clear()


@router.message(F.text, StateFilter(FSMUserInputName.fullname))
async def process_incorrect_input_name(message: Message) -> None:
    """Обработка некорректного ввода имени и фамилии."""
    await message.answer(
        text=(
            "Некорректный ввод!\n"
            "Ваше сообщение должно содержать имя и фамилию, разделенные пробелом."
            "\n\nПопробуйте еще раз"
        )
    )
