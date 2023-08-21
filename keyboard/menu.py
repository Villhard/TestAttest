"""Модуль для создания меню бота."""
from aiogram import Bot
from aiogram.types import BotCommand


async def set_menu(bot: Bot) -> None:
    """Настройка меню бота."""
    menu_commands = [
        BotCommand(command="/start", description="Старт"),
        BotCommand(command="/help", description="Помощь"),
    ]
    await bot.set_my_commands(commands=menu_commands)
