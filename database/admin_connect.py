"""Модуль для работы с базой данных для админов."""

from sqlalchemy.orm import sessionmaker

from database.database import Test, engine

Session = sessionmaker(engine)


def create_test(title: str, description: str) -> None:
    """Создание теста в базе данных."""
    with Session() as session:
        test = Test(title=title, description=description)
        session.add(test)
        session.commit()


def get_tests() -> list[Test]:
    """Получение всех тестов из базы данных."""
    with Session() as session:
        tests = session.query(Test).all()
        return tests
