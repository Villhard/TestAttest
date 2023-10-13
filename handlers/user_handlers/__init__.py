from aiogram import Router

from . import navigation, process_testing

router = Router()

router.include_router(navigation.router)
router.include_router(process_testing.router)
