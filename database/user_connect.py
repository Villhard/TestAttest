"""Модуль работы с базой данных для пользователей."""

from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker

from config import config
from database.database import (
    IncorrectAnswer,
    Question,
    Result,
    Test,
    User,
    engine,
)

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
                    Result.score > config.pass_score,
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


def save_result(
    user_id: int,
    test_id: int,
    result: dict[int, dict[int, bool]],
) -> None:
    """Сохранение результата теста в базу данных."""

    incorrect_answers = {}
    for question_id, answer in result.items():
        if not next(iter(answer.values())):
            incorrect_answers[question_id] = answer
    score = round((len(result) - len(incorrect_answers)) / len(result) * 100)

    with Session() as session:
        result = Result(user_id=user_id, test_id=test_id, score=score)
        session.add(result)
        session.commit()
        result_id = result.id

    with Session() as session:
        for question_id, answer in incorrect_answers.items():
            incorrect_answer = IncorrectAnswer(
                question_id=question_id,
                answer_id=next(iter(answer)),
                result_id=result_id,
            )
            session.add(incorrect_answer)
        session.commit()
    return score
