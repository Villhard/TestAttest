"""User handlers."""
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database import user_connect

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Command /start handler for user."""
    user = user_connect.check_user_exists(message.from_user.id)
    if user:
        await message.answer(text=f"Привет, {user.name}!")
    else:
        await message.answer(
            text=(
                "Добро пожаловать в бота для тестирования!"
                "\nВам нужно заполнить личные данные\n\n"
                "Введите ваше имя и фалимию"
            )
        )


@router.message(F.text)
async def save_user_in_db(message: Message) -> None:
    """Create user in DB."""
    name, surname = message.text.title().strip().split()
    user_connect.create_user(message.from_user.id, name, surname)
    await message.answer(text="Вы успешно зарегистрировались!")
