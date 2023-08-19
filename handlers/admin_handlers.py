"""Admin handlers."""
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import config

router = Router()

router.message.filter(F.from_user.id.in_(config.admin_ids))


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Command /start handler for admin."""
    await message.answer("Привет, админ!")
