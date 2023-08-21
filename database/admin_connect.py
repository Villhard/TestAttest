"""Модуль для работы с базой данных для админов."""

from sqlalchemy.orm import sessionmaker

from database.database import Question, Test, engine

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


def get_test_by_id(test_id: int) -> Test:
    """Получение теста по id."""
    with Session() as session:
        test = session.query(Test).filter(Test.id == test_id).first()
        return test


def get_questions_by_test_id(test_id: int) -> list[Question]:
    """Получение вопросов по id теста."""
    with Session() as session:
        questions = session.query(Question).filter(Question.test_id == test_id).all()
        return questions


def delete_test_by_id(test_id: int) -> None:
    """Удаление теста по id."""
    with Session() as session:
        session.query(Test).filter(Test.id == test_id).delete()
        session.commit()
