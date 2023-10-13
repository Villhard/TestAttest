from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from database import user_connect as db
from keyboard import keyboard_builder as kb
from config import lexicon
from states import FSMUserInputName

router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message, state: FSMContext):
    """Greeting user"""
    user = db.get_user(message.from_user.id)
    if user:
        keyboard = kb.create_main_menu_keyboard(
            is_admin=False,
        )
        await message.answer(
            text=f"{lexicon.MESSAGES['greeting user'].format(name=user.name)}",
            reply_markup=keyboard,
        )
    else:
        await message.answer(
            text=f"{lexicon.MESSAGES['greeting stranger']}"
        )
        await state.set_state(FSMUserInputName.fullname)


@router.callback_query(F.data == "main_menu", StateFilter(default_state))
async def call_main_menu(callback: CallbackQuery):
    """Main menu"""
    keyboard = kb.create_main_menu_keyboard(
        is_admin=False,
    )
    await callback.message.edit_text(
        text=f"{lexicon.MESSAGES['main menu']}",
        reply_markup=keyboard,
    )