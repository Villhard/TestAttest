from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.orm import relationship

from .base import BaseModel
from .question import Question
from .result import Result


class Test(BaseModel):
    """
    Модель теста.

    title: str - название теста.
    description: str - описание теста.
    is_publish: bool - опубликован ли тест.
    questions: list[Question] - вопросы теста.
    results: list[Result] - результаты теста.
    """

    __tablename__ = "tests"

    title: str = Column(String, nullable=False)
    description: str = Column(Text, nullable=False)
    is_published: bool = Column(Boolean, default=False, nullable=False)

    questions: list[Question] = relationship(
        "Question", back_populates="test", uselist=True
    )
    results: list[Result] = relationship(
        "Result", back_populates="test", uselist=True
    )
