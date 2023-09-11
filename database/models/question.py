from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import BaseModel


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

    text = Column(String, nullable=False)
    image = Column(String)

    test = relationship("Test", back_populates="questions", uselist=False)
    answers = relationship("Answer", back_populates="question", uselist=True)
    incorrect_answers = relationship(
        "IncorrectAnswer", back_populates="question", uselist=True
    )
