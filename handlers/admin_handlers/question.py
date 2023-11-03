import re

from aiogram import Router, F
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    PhotoSize,
)
from loguru import logger

from config import lexicon
from database import admin_connect as db
from handlers.admin_handlers.states import FSMCreateQuestions
import keyboard.keyboard_builder as kb
from utils import admin_utils as utils

router = Router()


@router.callback_query(
    lambda call: re.fullmatch(r"add_question_test_\d+", call.data),
    StateFilter(default_state),
)
async def call_add_question(callback: CallbackQuery, state: FSMContext):
    """Create question."""
    await state.update_data(test_id=int(callback.data.split("_")[3]))
    await state.update_data(answers=[])

    # DEBUG LOG
    logger.debug(
        lexicon.MESSAGES["add question"].format(
            admin_id=callback.from_user.id, test_id=callback.data.split("_")[3]
        )
    )

    await callback.message.edit_text(text=lexicon.MESSAGES["add question"])
    await state.set_state(FSMCreateQuestions.text)
    await callback.answer()


@router.message(F.text, StateFilter(FSMCreateQuestions.text))
async def process_input_question_text(message: Message, state: FSMContext):
    """Create question. Question text."""
    await state.update_data(text=message.text)
    await message.answer(text=lexicon.MESSAGES["add question answer 1"])
    await state.set_state(FSMCreateQuestions.answers)


@router.message(F.text, StateFilter(FSMCreateQuestions.answers))
async def process_input_answers_text(message: Message, state: FSMContext):
    """Create question. Answers text."""
    data = await state.get_data()
    answers = data["answers"]
    answers.append(message.text)
    await state.update_data(answers=answers)
    if len(answers) < 4:
        await message.answer(
            text=lexicon.MESSAGES["add question answer n"].format(n=len(answers) + 1)
        )
    else:
        keyboard = kb.create_choice_answer_keyboard(answers)
        await message.answer(
            text=lexicon.MESSAGES["confirm correct answer"],
            reply_markup=keyboard,
        )


@router.callback_query(F.data, StateFilter(FSMCreateQuestions.answers))
async def process_input_correct_answer(callback: CallbackQuery, state: FSMContext):
    """Create question. Correct answer."""
    data = await state.get_data()
    await state.update_data(
        answers={
            answer: is_correct
            for answer in data["answers"]
            for is_correct in [True if answer == callback.data else False]
        }
    )
    keyboard = [
        [InlineKeyboardButton(text=lexicon.BUTTONS["skip"], callback_data="skip")]
    ]
    await callback.message.edit_text(
        text=lexicon.MESSAGES["add question image"],
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )
    await state.set_state(FSMCreateQuestions.image)
    await callback.answer()


@router.message(F.photo, StateFilter(FSMCreateQuestions.image))
async def process_input_image_question(message: Message, state: FSMContext):
    """Create question. Image question."""
    data = await state.get_data()
    test_id = data["test_id"]
    question = data["text"]
    answers = data["answers"]
    photo: PhotoSize = message.photo[-1]
    photo_path = photo.file_id
    number_image = utils.get_next_number_image(test_id)
    await message.bot.download(
        photo_path,
        destination=f"img/test_{test_id}/img_{number_image}.jpg",
    )
    db.create_question(
        test_id=test_id,
        text=question,
        answers=answers,
        image=f"img_{number_image}.jpg",
    )
    test = db.get_test_by_id(test_id)
    keyboard = kb.create_test_menu_keyboard(
        test=test,
        questions=db.get_questions_by_test_id(test_id),
        is_publish=test.is_publish,
    )
    await message.answer(
        text=lexicon.MESSAGES["question created"],
        reply_markup=keyboard,
    )
    await state.clear()
    await state.set_state(default_state)


@router.callback_query(F.data, StateFilter(FSMCreateQuestions.image))
async def process_skip_image_question(callback: CallbackQuery, state: FSMContext):
    """Create question. Skip image."""
    data = await state.get_data()
    test_id = data["test_id"]
    question = data["text"]
    answers = data["answers"]
    db.create_question(
        test_id=test_id,
        text=question,
        answers=answers,
    )
    test = db.get_test_by_id(test_id)
    keyboard = kb.create_test_menu_keyboard(
        test=test,
        questions=db.get_questions_by_test_id(test_id),
        is_publish=test.is_publish,
    )
    await callback.message.edit_text(
        text=lexicon.MESSAGES["question created"],
        reply_markup=keyboard,
    )
    await state.clear()
    await state.set_state(default_state)
    await callback.answer()
