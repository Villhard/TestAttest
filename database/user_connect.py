"""
Модуль работы с базой данных для пользователей.

Содержит функции для работы с базой данных для пользователей.

Функции:
    get_user:
        Получение пользователя из базы данных.
    create_user:
        Создание пользователя в базе данных.
    get_tests:
        Получение тестов для прохождения из базы данных.
    get_test:
        Получение теста из базы данных.
    get_questions:
        Получение вопросов из базы данных.
    save_result:
        Сохранение результата теста в базу данных.
    get_answers_by_question_id:
        Получение ответов по id вопроса из базы данных.
    get_answer_by_id:
        Получение ответа по id ответа из базы данных.
"""

from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker

from config import config
from database.database import (
    IncorrectAnswer,
    Question,
    Result,
    Test,
    User,
    Answer,
    engine,
)

Session = sessionmaker(engine)


def get_user(tg_id: int) -> User | None:
    """
    Получение пользователя из базы данных.

    Args:
        tg_id:
            Идентификатор пользователя в Telegram.

    Returns:
        Пользователь.
    """
    with Session() as session:
        user = session.query(User).filter(User.tg_id == tg_id).one()
        return user


def create_user(tg_id: int, name: str, surname: str) -> None:
    """
    Создание пользователя в базе данных.

    Args:
        tg_id:
            Идентификатор пользователя в Telegram.
        name:
            Имя пользователя.
        surname:
            Фамилия пользователя.
    """
    with Session() as session:
        user = User(tg_id=tg_id, name=name, surname=surname)
        session.add(user)
        session.commit()


def get_tests(tg_id: int) -> list[Test]:
    """
    Получение тестов для прохождения из базы данных.

    Args:
        tg_id:
            Идентификатор пользователя в Telegram.

    Returns:
        Список тестов.
    """
    with Session() as session:
        user_id = session.query(User.id).filter(User.tg_id == tg_id).scalar()
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
    """
    Получение теста из базы данных.

    Args:
        test_id:
            Идентификатор теста.

    Returns:
        Тест.
    """
    with Session() as session:
        test = session.query(Test).filter(Test.id == test_id).one()
        return test


def get_questions(test_id: int) -> list[Question]:
    """
    Получение вопросов из базы данных.

    Args:
        test_id:
            Идентификатор теста.

    Returns:
        Список вопросов.
    """
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
    """
    Сохранение результата теста в базу данных.

    Args:
        user_id:
            Идентификатор пользователя.
        test_id:
            Идентификатор теста.
        result:
            Результат теста.
    """

    incorrect_answers = [
        (question_id, next(iter(answer)))
        for question_id, answer in result.items()
        if not next(iter(answer.values()))
    ]

    score = round((len(result) - len(incorrect_answers)) / len(result) * 100)

    with Session() as session:
        result_obj = Result(user_id=user_id, test_id=test_id, score=score)
        session.add(result_obj)

        session.commit()

        incorrect_answer_objs = [
            IncorrectAnswer(
                question_id=question_id,
                answer_id=answer_id,
                result_id=result_obj.id,
            )
            for question_id, answer_id in incorrect_answers
        ]

        session.add_all(incorrect_answer_objs)

        session.commit()

    return score


def get_answers_by_question_id(
    question_id: int,
) -> list[Answer]:
    """
    Получение ответов по id вопроса из базы данных.

    Args:
        question_id:
            Идентификатор вопроса.

    Returns:
        Список ответов.
    """
    with Session() as session:
        answers = (
            session.query(Answer)
            .filter(Answer.question_id == question_id)
            .order_by(Answer.id)
            .all()
        )
        return answers


def get_answer_by_id(
    answer_id: int,
) -> Answer:
    """
    Получение ответа по id из базы данных.

    Args:
        answer_id:
            Идентификатор ответа.

    Returns:
        Ответ.
    """
    with Session() as session:
        answer = session.query(Answer).filter(Answer.id == answer_id).one()
        return answer
