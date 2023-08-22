"""
Модуль для работы с базой данных.

Содержит в себе описание таблиц и их связей.
"""
from sqlalchemy import BigInteger, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    mapped_column,
    relationship,
)

from config import config

engine = create_engine(config.database.url)

# Создание базовой модели
Base = declarative_base()


class User(Base):
    """Модель пользователя."""

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(  # noqa: A003
        primary_key=True, autoincrement=True
    )
    tg_id = mapped_column(BigInteger, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    results: Mapped[list["Result"]] = relationship(
        back_populates="user", uselist=True, lazy="joined"
    )


class Test(Base):
    """Модель теста."""

    __tablename__ = "tests"
    id: Mapped[int] = mapped_column(  # noqa: A003
        primary_key=True, autoincrement=True
    )
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    questions: Mapped[list["Question"]] = relationship(
        back_populates="test", uselist=True, lazy="joined"
    )
    results: Mapped[list["Result"]] = relationship(
        back_populates="test", uselist=True, lazy="joined"
    )
    is_publish: Mapped[bool] = mapped_column(nullable=False, default=False)


class Question(Base):
    """Модель вопроса."""

    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(  # noqa: A003
        primary_key=True, autoincrement=True
    )
    test: Mapped["Test"] = relationship(
        back_populates="questions", uselist=False
    )
    test_id = mapped_column(ForeignKey("tests.id"), nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(nullable=True, default="default")
    answers: Mapped[str] = mapped_column(nullable=False)


class Result(Base):
    """Модель результата."""

    __tablename__ = "results"
    id: Mapped[int] = mapped_column(  # noqa: A003
        primary_key=True, autoincrement=True
    )
    test: Mapped["Test"] = relationship(
        back_populates="results", uselist=False
    )
    test_id = mapped_column(ForeignKey("tests.id"), nullable=False)
    user: Mapped["User"] = relationship(
        back_populates="results", uselist=False
    )
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    score: Mapped[int] = mapped_column(nullable=False)
    datetime_start = mapped_column(DateTime, nullable=False)
    datetime_end = mapped_column(DateTime, nullable=False)
    incorrect_answers: Mapped[str] = mapped_column(nullable=True)


Base.metadata.create_all(engine)
