from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from .base import BaseModel


class Result(BaseModel):
    """
    Модель результата.

    score: int - количество правильных ответов.
    test: Test - тест, к которому относится результат.
    user: User - пользователь, к которому относится результат.
    incorrect_answers: list[IncorrectAnswer] - неправильные ответы на вопрос.
    """

    __tablename__ = "results"

    score = Column(Integer, nullable=False)

    test = relationship("Test", back_populates="results", uselist=False)
    user = relationship("User", back_populates="results", uselist=False)
    incorrect_answers = relationship(
        "IncorrectAnswer", back_populates="result", uselist=True
    )
