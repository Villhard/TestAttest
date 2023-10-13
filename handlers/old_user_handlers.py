import re

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, FSInputFile, Message

from config import config
from database import user_connect as db
from keyboard import keyboard_builder as kb

router = Router()


# =============================================================================
# =========== ПРОЦЕСС ПРОХОЖДЕНИЯ ТЕСТА =======================================
# =============================================================================


@router.callback_query(
    lambda call: re.fullmatch(r"start_test_\d+", call.data),
    StateFilter(default_state),
)
async def call_start_test(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    """Начало теста."""
    await state.set_state(FSMTesting.testing)
    test_id = int(callback.data.split("_")[2])
    await state.update_data(test_id=test_id)
    questions = db.get_questions(test_id)
    await state.update_data(questions=questions)
    await state.update_data(result={})
    question = questions.pop(0)
    await state.update_data(question_id=question.id)
    answers = db.get_answers_by_question_id(question.id)
    await state.update_data(answers=answers)
    keyboard = kb.create_test_answers_keyboard(
        answers=answers,
    )
    if question.image:
        image = FSInputFile(f"img/test_{test_id}/{question.image}")
        await callback.message.answer_photo(
            photo=image,
            caption=question.text,
            reply_markup=keyboard,
        )
        await callback.message.delete()
    else:
        await callback.message.edit_text(
            text=question.text,
            reply_markup=keyboard,
        )


@router.callback_query(F.data, StateFilter(FSMTesting.testing))
async def call_answering(callback: CallbackQuery, state: FSMContext):
    """Процесс прохождения теста."""
    data = await state.get_data()
    result = data["result"]
    answer = db.get_answer_by_id(callback.data)
    if answer.is_correct:
        result[data["question_id"]] = {answer.id: True}
    else:
        result[data["question_id"]] = {answer.id: False}

    if data["questions"]:
        question = data["questions"].pop(0)
        await state.update_data(question_id=question.id)
        answers = db.get_answers_by_question_id(question.id)
        await state.update_data(answers=answers)
        keyboard = kb.create_test_answers_keyboard(
            answers=answers,
        )
        if question.image:
            image = FSInputFile(f"img/test_{data['test_id']}/{question.image}")
            await callback.message.answer_photo(
                photo=image,
                caption=question.text,
                reply_markup=keyboard,
            )
            await callback.message.delete()
        else:
            await callback.message.answer(
                text=question.text,
                reply_markup=keyboard,
            )
            await callback.message.delete()
    else:
        score = db.save_result(
            user_id=db.get_user(callback.from_user.id).id,
            test_id=data["test_id"],
            result=result,
        )
        await state.clear()
        await state.set_state(default_state)
        keyboard = kb.create_after_test_keyboard()
        await callback.message.answer(
            text=(
                f"Тест пройден!\nВы набрали: {score} баллов"
                if score >= config.pass_score
                else f"Тест не пройден!\nВы набрали: {score} баллов\n\n"
                "Попробуйте еще раз"
            ),
            reply_markup=keyboard,
        )
        await callback.message.delete()
