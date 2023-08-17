from aiogram import Router, F
from aiogram.types import (
    Message,
)
from aiogram.filters import CommandStart
from config import config

router = Router()

router.message.filter(F.from_user.id.in_(config.admin_ids))


@router.message(CommandStart())
async def cmd_start(message: Message):
    """/start command handler for admins"""
    await message.answer("Привет, админ!")
