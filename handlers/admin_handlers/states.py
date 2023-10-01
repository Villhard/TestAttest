from aiogram.filters.state import State, StatesGroup


class FSMCreateTest(StatesGroup):
    title = State()
    description = State()


class FSMCreateQuestions(StatesGroup):
    text = State()
    answers = State()
    image = State()
