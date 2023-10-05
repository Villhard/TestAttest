from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery
from loguru import logger

from config import lexicon
from handlers.admin_handlers.states import FSMCreateTest

router = Router()


@router.callback_query(F.data == "add_test", StateFilter(default_state))
async def call_add_test(callback: CallbackQuery, state: FSMContext):
    """Start create test"""

    # DEBUG LOG
    logger.debug(
        f"{lexicon.LOGS['add test'].format(admin_id=callback.from_user.id)}"
    )

    await callback.message.edit_text(text=f"{lexicon.MESSAGES['add test']}")
    await state.set_state(FSMCreateTest.title)
