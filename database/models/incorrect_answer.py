from sqlalchemy.orm import relationship

from .base import BaseModel


class IncorrectAnswer(BaseModel):
    """
    Модель неправильного ответа.

    result: Result - результат, к которому относится неправильный ответ.
    question: Question - вопрос, к которому относится неправильный ответ.
    answer: Answer - ответ, к которому относится неправильный ответ.
    """

    __tablename__ = "incorrect_answers"

    result = relationship(
        "Result", back_populates="incorrect_answers", uselist=False
    )
    question = relationship(
        "Question", back_populates="incorrect_answers", uselist=False
    )
    answer = relationship(
        "Answer", back_populates="incorrect_answers", uselist=False
    )
