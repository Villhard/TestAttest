from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from .base import BaseModel
from .test import Test
from .user import User
from .incorrect_answer import IncorrectAnswer


class Result(BaseModel):
    """
    Модель результата.

    score: int - количество правильных ответов.
    test: Test - тест, к которому относится результат.
    user: User - пользователь, к которому относится результат.
    incorrect_answers: list[IncorrectAnswer] - неправильные ответы на вопрос.
    """

    __tablename__ = "results"

    score: int = Column(Integer, nullable=False)

    test: Test = relationship("Test", back_populates="results", uselist=False)
    user: User = relationship("User", back_populates="results", uselist=False)
    incorrect_answers: list[IncorrectAnswer] = relationship(
        "IncorrectAnswer", back_populates="result", uselist=True
    )
