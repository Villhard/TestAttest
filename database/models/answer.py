from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from .base import BaseModel


class Answer(BaseModel):
    """
    Модель ответа.

    text: str - текст ответа.
    is_correct: bool - является ли ответ правильным.
    question: Question - вопрос, к которому относится ответ.
    incorrect_answers: list[IncorrectAnswer] - неправильные ответы на вопрос.
    """

    __tablename__ = "answers"

    text = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)

    question = relationship(
        "Question", back_populates="answers", uselist=False
    )
    incorrect_answers = relationship(
        "IncorrectAnswer", back_populates="answer", uselist=True
    )
