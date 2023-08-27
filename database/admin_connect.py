"""Модуль для работы с базой данных для админов."""
from sqlalchemy.orm import sessionmaker

from database.database import (
    Answer,
    IncorrectAnswer,
    Question,
    Result,
    User,
    Test,
    engine,
)
from config import config

Session = sessionmaker(engine)


def create_test(title: str, description: str) -> None:
    """Создание теста в базе данных."""
    with Session() as session:
        test = Test(
            title=title,
            description=description,
        )
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
        questions = (
            session.query(Question).filter(Question.test_id == test_id).all()
        )
        return questions


def delete_test_by_id(test_id: int) -> None:
    """Удаление теста и всех его связей по id."""
    with Session() as session:
        session.query(IncorrectAnswer).filter(
            IncorrectAnswer.result.has(test_id=test_id)
        ).delete()
        session.query(Result).filter(Result.test_id == test_id).delete()
        session.query(Answer).filter(
            Answer.question.has(test_id=test_id)
        ).delete()
        session.query(Question).filter(Question.test_id == test_id).delete()
        session.query(Test).filter(Test.id == test_id).delete()
        session.commit()


def publish_test_by_id(test_id: int) -> None:
    """Публикация теста по id."""
    with Session() as session:
        session.query(Test).filter(Test.id == test_id).update(
            {"is_publish": True}
        )
        session.commit()


def create_question(  # TODO: Оптимизировать создание вопроса с ответами.
    test_id: int,
    text: str,
    answers: dict[str, bool],
    image: str,
) -> None:
    """Создание вопроса в базе данных."""
    with Session() as session:
        question = Question(
            test_id=test_id,
            text=text,
            image=image,
        )
        session.add(question)
        session.commit()
        create_answers(question_id=question.id, answers=answers)


def create_answers(
    question_id: int,
    answers: dict[str, bool],
) -> None:
    """Создание ответов в базе данных."""
    with Session() as session:
        for text in answers:
            answer = Answer(
                question_id=question_id,
                text=text,
                is_correct=answers[text],
            )
            session.add(answer)
        session.commit()


def get_statistics_by_test_id(test_id: int) -> dict[str, int]:
    """Получение статистики по тесту."""
    with Session() as session:
        results = session.query(Result).filter(Result.test_id == test_id)

        total = results.count()
        completed = results.filter(Result.score >= config.pass_score).count()

        statistics = {"total": total, "completed": completed}

        return statistics


def get_users() -> list[User]:
    """Получение всех пользователей из базы данных."""
    with Session() as session:
        users = session.query(User).all()
        return users


def get_user_by_id(user_id: int) -> User:
    """Получение пользователя по id."""
    with Session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        return user


def get_results_by_user_id(user_id: int) -> dict[str, int]:
    """Получение результатов пользователя по id."""
    with Session() as session:
        total_tests = session.query(Test).count()
        completed_tests = (
            session.query(Result)
            .filter(Result.user_id == user_id)
            .group_by(Result.test_id)
            .filter(Result.score >= config.pass_score)
            .count()
        )
        return {"total": total_tests, "completed": completed_tests}
