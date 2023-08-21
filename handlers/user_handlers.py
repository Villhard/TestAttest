"""User handlers."""
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database import user_connect

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """
    Обработчик команды /start.

    Handler проверяет наличие пользователя в базе данных,
    и если он есть, то приветствует его по имени, иначе
    предлагает ввести имя и фамилию.
    """
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
    """
    Сохранение пользователя в базе данных.

    Handler обрабатывает введенное имя и фамилию пользователя,
    и сохраняет их в базе данных. Имя и фамилия должны быть
    разделены пробелом.
    """
    name, surname = message.text.title().strip().split()
    user_connect.create_user(message.from_user.id, name, surname)
    await message.answer(text="Вы успешно зарегистрировались!")
