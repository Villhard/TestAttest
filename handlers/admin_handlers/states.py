from aiogram.filters.state import State, StatesGroup


class FSMCreateTest(StatesGroup):
    """
    Represents the states for creating a test.

    States:
        - title: Represents the state for capturing the title of the
        test.
        - description: Represents the state for capturing the
        description of the test.
    """

    title = State()
    description = State()


class FSMCreateQuestions(StatesGroup):
    """
    Represents the states for creating questions.

    States:
        - text: Represents the state for capturing the text of the
        question.
        - answers: Represents the state for capturing the answers to
        the question.
        - image: Represents the state for capturing an image related
        to the question.
    """

    text = State()
    answers = State()
    image = State()
