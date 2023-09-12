from sqlalchemy.orm import relationship

from .answer import Answer
from .base import BaseModel
from .question import Question
from .result import Result


class IncorrectAnswer(BaseModel):
    """
    Модель неправильного ответа.

    result: Result - результат, к которому относится неправильный ответ.
    question: Question - вопрос, к которому относится неправильный ответ.
    answer: Answer - ответ, к которому относится неправильный ответ.
    """

    __tablename__ = "incorrect_answers"

    result: Result = relationship(
        "Result", back_populates="incorrect_answers", uselist=False
    )
    question: Question = relationship(
        "Question", back_populates="incorrect_answers", uselist=False
    )
    answer: Answer = relationship(
        "Answer", back_populates="incorrect_answers", uselist=False
    )
