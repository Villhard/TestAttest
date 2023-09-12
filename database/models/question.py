from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from .base import BaseModel
from .test import Test
from .answer import Answer
from .incorrect_answer import IncorrectAnswer


class Question(BaseModel):
    """
    Модель вопроса.

    text: str - текст вопроса.
    image: str - изображение вопроса.
    test: Test - тест, к которому относится вопрос.
    answers: list[Answer] - ответы на вопрос.
    incorrect_answers: list[IncorrectAnswer] - неправильные ответы на вопрос.
    """

    __tablename__ = "questions"

    text: str = Column(Text, nullable=False)
    image: str = Column(String)

    test: Test = relationship("Test", back_populates="questions", uselist=False)
    answers: list[Answer] = relationship("Answer", back_populates="question", uselist=True)
    incorrect_answers: list[IncorrectAnswer] = relationship(
        "IncorrectAnswer", back_populates="question", uselist=True
    )
