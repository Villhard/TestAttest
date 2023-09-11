from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from .base import BaseModel


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

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    is_published = Column(Boolean, default=False, nullable=False)

    questions = relationship("Question", back_populates="test", uselist=True)
    results = relationship("Result", back_populates="test", uselist=True)
