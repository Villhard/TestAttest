"""Модуль работы с базой данных для пользователей."""

from sqlalchemy.orm import sessionmaker

from database.database import Result, Test, User, engine

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
            .join(Result, Test.id == Result.test_id)
            .filter(Result.user_id != user_id)
            .filter(Result.score < 70)
            .all()
        )
        return tests
