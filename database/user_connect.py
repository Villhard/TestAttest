"""Модуль работы с базой данных для пользователей."""

from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker

from database.database import Result, Test, User, engine, Question

Session = sessionmaker(engine)


def get_user(tg_id: int) -> User | None:
    """Получение пользователя из базы данных."""
    with Session() as session:
        user = session.query(User).filter(User.tg_id == tg_id).first()
        return user


def create_user(tg_id: int, name: str, surname: str) -> None:
    """Создание пользователя в базе данных."""
    with Session() as session:
        user = User(tg_id=tg_id, name=name, surname=surname)
        session.add(user)
        session.commit()


def get_tests(tg_id: int) -> list[Test]:
    """Получение тестов для прохождения из базы данных."""
    with Session() as session:
        user_id = session.query(User.id).filter(User.tg_id == tg_id).first()[0]
        tests = (
            session.query(Test)
            .outerjoin(
                Result,
                and_(
                    Result.test_id == Test.id,
                    Result.user_id == user_id,
                    Result.score > 70,
                ),
            )
            .filter(Test.is_publish)
            .filter(Result.id.is_(None))
            .all()
        )
        return tests


def get_test(test_id: int) -> Test:
    """Получение теста из базы данных."""
    with Session() as session:
        test = session.query(Test).filter(Test.id == test_id).first()
        return test


def get_questions(test_id: int) -> list[Question]:
    """Получение вопросов из базы данных."""
    with Session() as session:
        questions = (
            session.query(Question)
            .filter(Question.test_id == test_id)
            .order_by(Question.id)
            .all()
        )
        return questions
