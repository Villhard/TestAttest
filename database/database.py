"""Module for create database."""
from sqlalchemy import BigInteger, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

engine = create_engine("sqlite:///database.db")


class Base(DeclarativeBase):
    """Base class."""

    pass


class User(Base):
    """User class."""

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # noqa: A003
    tg_id = mapped_column(BigInteger, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    results: Mapped[list["Result"]] = relationship(
        back_populates="user", uselist=True, lazy="joined"
    )


class Test(Base):
    """Test class."""

    __tablename__ = "tests"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # noqa: A003
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    questions: Mapped[list["Question"]] = relationship(
        back_populates="test", uselist=True, lazy="joined"
    )
    results: Mapped[list["Result"]] = relationship(
        back_populates="test", uselist=True, lazy="joined"
    )


class Question(Base):
    """Question class."""

    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # noqa: A003
    test: Mapped["Test"] = relationship(back_populates="questions", uselist=False)
    test_id = mapped_column(ForeignKey("tests.id"), nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    answers: Mapped[list["Answer"]] = relationship(
        back_populates="question", uselist=True, lazy="joined"
    )
    image: Mapped["Image"] = relationship(back_populates="question", uselist=False)
    incorrect_answers: Mapped[list["Incorrect_Answer"]] = relationship(
        back_populates="question", uselist=True, lazy="joined"
    )


class Answer(Base):
    """Answer class."""

    __tablename__ = "answers"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # noqa: A003
    question: Mapped["Question"] = relationship(back_populates="answers", uselist=False)
    question_id = mapped_column(ForeignKey("questions.id"), nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    is_correct: Mapped[bool] = mapped_column(nullable=False)


class Image(Base):
    """Image class."""

    __tablename__ = "images"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # noqa: A003
    question: Mapped["Question"] = relationship(back_populates="image", uselist=False)
    question_id = mapped_column(ForeignKey("questions.id"), nullable=False)
    path: Mapped[str] = mapped_column(nullable=False)


class Result(Base):
    """Result class."""

    __tablename__ = "results"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # noqa: A003
    test: Mapped["Test"] = relationship(back_populates="results", uselist=False)
    test_id = mapped_column(ForeignKey("tests.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="results", uselist=False)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    score: Mapped[int] = mapped_column(nullable=False)
    datetime_start = mapped_column(DateTime, nullable=False)
    datetime_end = mapped_column(DateTime, nullable=False)
    incorrect_answers: Mapped[list["Incorrect_Answer"]] = relationship(
        back_populates="result", uselist=True, lazy="joined"
    )


class Incorrect_Answer(Base):
    """Incorrect_Answer class."""

    __tablename__ = "incorrect_answers"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # noqa: A003
    result: Mapped["Result"] = relationship(back_populates="incorrect_answers", uselist=False)
    result_id = mapped_column(ForeignKey("results.id"), nullable=False)
    question: Mapped["Question"] = relationship(back_populates="incorrect_answers", uselist=False)
    question_id = mapped_column(ForeignKey("questions.id"), nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)


Base.metadata.create_all(engine)
