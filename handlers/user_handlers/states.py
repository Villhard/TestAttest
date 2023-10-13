from aiogram.fsm.state import StatesGroup, State


class FSMUserInputName(StatesGroup):
    fullname = State()


class FSMTesting(StatesGroup):
    testing = State()
