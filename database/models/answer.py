from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from .base import BaseModel
from .question import Question
from .incorrect_answer import IncorrectAnswer


class Answer(BaseModel):
    """
    Модель ответа.

    text: str - текст ответа.
    is_correct: bool - является ли ответ правильным.
    question: Question - вопрос, к которому относится ответ.
    incorrect_answers: list[IncorrectAnswer] - неправильные ответы на вопрос.
    """

    __tablename__ = "answers"

    text: str = Column(String, nullable=False)
    is_correct: bool = Column(Boolean, nullable=False)

    question: Question = relationship(
        "Question", back_populates="answers", uselist=False
    )
    incorrect_answers: list[IncorrectAnswer] = relationship(
        "IncorrectAnswer", back_populates="answer", uselist=True
    )
