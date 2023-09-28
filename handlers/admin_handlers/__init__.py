from aiogram import F, Router

from config import config
from . import navigation

router = Router()

router.callback_query.filter(F.from_user.id.in_(config.bot.admin_ids))
router.message.filter(F.from_user.id.in_(config.bot.admin_ids))

router.include_router(navigation.router)
