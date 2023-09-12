from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import relationship

from .base import BaseModel
from .result import Result


class User(BaseModel):
    """
    Модель пользователя.

    tg_id: int - id пользователя в Telegram.
    name: str - имя пользователя.
    surname: str - фамилия пользователя.
    results: list[Result] - результаты пользователя.
    """

    __tablename__ = "users"

    tg_id: int = Column(BigInteger, unique=True, nullable=False)
    name: str = Column(String, nullable=False)
    surname: str = Column(String, nullable=False)

    results: list[Result] = relationship(
        "Result", back_populates="user", uselist=True
    )
