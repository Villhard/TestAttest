"""
Модуль для работы с базой данных для админов.

Содержит функции для создания, удаления, публикации тестов,
создания вопросов с ответами, получения статистики по тестам,
получения пользователей и их результатов.

Функции:
    create_test:
        Создание теста в базе данных.
    get_tests:
        Получение всех тестов из базы данных.
    get_test_by_id:
        Получение теста по id.
    get_questions_by_test_id:
        Получение вопросов по id теста.
    delete_test_by_id:
        Удаление теста и всех его связей по id.
    publish_test_by_id:
        Публикация теста по id.
    create_question:
        Создание вопроса с ответами в базе данных.
    get_statistics_by_test_id:
        Получение статистики по тесту.
    get_users:
        Получение всех пользователей из базы данных.
    get_user_by_id:
        Получение пользователя по id.
    get_results_by_user_id:
        Получение результатов пользователя по id.
    get_question_by_id:
        Получение вопроса по id.
    change_correct_answer:
        Изменение правильного ответа.
    get_test_id_by_question_id:
        Получение id теста по id вопроса.
"""
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
    """
    Создание теста в базе данных.

    Args:
        title:
            Название теста.
        description:
            Описание теста.
    """
    with Session() as session:
        test = Test(
            title=title,
            description=description,
        )
        session.add(test)
        session.commit()


def get_tests() -> list[Test]:
    """
    Получение всех тестов из базы данных.

    Returns:
        Список тестов.
    """
    with Session() as session:
        tests = session.query(Test).all()
        return tests


def get_test_by_id(test_id: int) -> Test:
    """
    Получение теста по id.

    Args:
        test_id:
            id теста.

    Returns:
        Тест.
    """
    with Session() as session:
        test = session.query(Test).filter(Test.id == test_id).first()
        return test


def get_questions_by_test_id(test_id: int) -> list[Question]:
    """
    Получение вопросов по id теста.

    Args:
        test_id:
            id теста.

    Returns:
        Список вопросов.
    """
    with Session() as session:
        questions = (
            session.query(Question).filter(Question.test_id == test_id).all()
        )
        return questions


def delete_test_by_id(test_id: int) -> None:
    """
    Удаление теста и всех его связей по id.

    Args:
        test_id:
            id теста.
    """
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
    """
    Публикация теста по id.

    Args:
        test_id:
            id теста.
    """
    with Session() as session:
        session.query(Test).filter(Test.id == test_id).update(
            {"is_publish": True}
        )
        session.commit()


def create_question(
    test_id: int, text: str, answers: dict[str, bool], image: str | None = None
) -> None:
    """
    Создание вопроса с ответами в базе данных.

    Args:
        test_id:
            id теста.
        text:
            Текст вопроса.
        answers:
            Словарь с ответами.
        image:
            Ссылка на изображение.
            По умолчанию None.
    """
    with Session() as session:
        question = Question(test_id=test_id, text=text, image=image)

        session.add(question)
        session.commit()

        answer_objs = [
            Answer(
                question_id=question.id,
                text=text,
                is_correct=is_correct,
            )
            for text, is_correct in answers.items()
        ]

        session.add_all(answer_objs)
        session.commit()


def get_statistics_by_test_id(test_id: int) -> dict[str, int]:
    """
    Получение статистики по тесту.

    Args:
        test_id:
            id теста.

    Returns:
        Словарь со статистикой.
    """
    with Session() as session:
        results = session.query(Result).filter(Result.test_id == test_id)

        total = results.count()
        completed = results.filter(Result.score >= config.pass_score).count()

        statistics = {"total": total, "completed": completed}

        return statistics


def get_users() -> list[User]:
    """
    Получение всех пользователей из базы данных.

    Returns:
        Список пользователей.
    """
    with Session() as session:
        users = session.query(User).all()
        return users


def get_user_by_id(user_id: int) -> User:
    """
    Получение пользователя по id.

    Args:
        user_id:
            id пользователя.

    Returns:
        Пользователь.
    """
    with Session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        return user


def get_results_by_user_id(user_id: int) -> dict[str, int]:
    """
    Получение результатов пользователя по id.

    Args:
        user_id:
            id пользователя.

    Returns:
        Словарь с результатами.
    """
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


def get_question_by_id(question_id: int) -> Question:
    """
    Получение вопроса по id.

    Args:
        question_id:
            id вопроса.

    Returns:
        Вопрос.
    """
    with Session() as session:
        question = (
            session.query(Question).filter(Question.id == question_id).first()
        )
        answers = (
            session.query(Answer)
            .filter(Answer.question_id == question.id)
            .all()
        )
        return question, answers


def change_correct_answer(
        question_id: int,
        answer_id: int,
) -> None:
    """
    Изменение правильного ответа.

    Args:
        question_id:
            id вопроса.
        answer_id:
            id ответа.
    """
    with Session() as session:
        session.query(Answer).filter(Answer.question_id == question_id).update(
            {"is_correct": False}
        )
        session.query(Answer).filter(Answer.id == answer_id).update(
            {"is_correct": True}
        )
        session.commit()


def get_test_id_by_question_id(question_id: int) -> int:
    """
    Получение id теста по id вопроса.

    Args:
        question_id:
            id вопроса.

    Returns:
        id теста.
    """
    with Session() as session:
        test_id = (
            session.query(Question)
            .filter(Question.id == question_id)
            .first()
            .test_id
        )
        return test_id
