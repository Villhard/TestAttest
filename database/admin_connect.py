"""
Модуль для работы с базой данных для админа.

Содержит функции для создания, удаления, публикации тестов,
создания вопросов с ответами, получения статистики по тестам,
получения пользователей и их результатов.

# TODO: Разделить на модули

Функции для работы с тестами:
    create_test
        Создание теста
    get_tests
        Получение всех тестов
    get_test_by_id
        Получение теста по id
    delete_test_by_id
        Удаление теста по id
    publish_test_by_id
        Публикация теста по id
    get_test_by_question_id
        Получение теста по id вопроса
    get_test_id_by_question_id
        Получение id теста по id вопроса
    get_statistics_by_test_id
        Получение статистики по id теста

Функции для работы с вопросами:
    create_question
        Создание вопроса с ответами
    get_question_by_id
        Получение вопроса по id
    get_questions_by_test_id
        Получение вопросов по id теста
    delete_question_by_id
        Удаление вопроса по id
    change_correct_answer
        Изменение правильного ответа

Функции для работы с пользователями:
    get_users
        Получение всех пользователей
    get_user_by_id
        Получение пользователя по id

Функции работы с результатами:
    get_count_results_by_user_id
        Получение количество результатов пользователя
    get_results_by_user_id
        Получение результатов пользователя
    get_result_by_id
        Получение результата по id
    get_result_data_by_result
        Получение данных результата
"""
from sqlalchemy.orm import sessionmaker, aliased

from config import config
from database.database import (
    Answer,
    IncorrectAnswer,
    Question,
    Result,
    User,
    Test,
    engine,
)

Session = sessionmaker(engine)


def get_session() -> Session:
    """Получение сессии для работы с базой данных."""
    with Session() as session:
        return session


def create_test(
    title: str, description: str, session: Session = get_session()
) -> None:
    """
    Создание теста в базе данных.

    Args:
        title:
            Название теста
        description:
            Описание теста
        session:
            Сессия
    """
    test = Test(
        title=title,
        description=description,
    )
    session.add(test)
    session.commit()


def get_tests(session: Session = get_session()) -> list[Test]:
    """
    Получение всех тестов из базы данных.

    Args:
        session:
            Сессия

    Returns:
        Список тестов
    """
    tests = session.query(Test).order_by(Test.id.desc()).all()
    return tests


def get_test_by_id(test_id: int, session: Session = get_session()) -> Test:
    """
    Получение теста по id.

    Args:
        test_id:
            id теста
        session:
            Сессия

    Returns:
        Тест
    """
    test = session.query(Test).filter(Test.id == test_id).one()
    return test


def delete_test_by_id(test_id: int, session: Session = get_session()) -> None:
    """
    Удаление теста и всех его связей по id.

    Args:
        test_id:
            id теста
        session:
            Сессия
    """
    session.query(IncorrectAnswer).filter(
        IncorrectAnswer.result.has(test_id=test_id)
    ).delete()
    session.query(Result).filter(Result.test_id == test_id).delete()
    session.query(Answer).filter(Answer.question.has(test_id=test_id)).delete()
    session.query(Question).filter(Question.test_id == test_id).delete()
    session.query(Test).filter(Test.id == test_id).delete()
    session.commit()


def publish_test_by_id(test_id: int) -> None:
    """
    Публикация теста по id.

    Args:
        test_id:
            id теста
    """
    with Session() as session:
        session.query(Test).filter(Test.id == test_id).update(
            {"is_publish": True}
        )
        session.commit()


def get_test_by_question_id(question_id: int) -> Test:
    """
    Получение теста по id вопроса.

    Args:
        question_id:
            id вопроса

    Returns:
        Тест
    """
    with Session() as session:
        test = (
            session.query(Test)
            .filter(Test.id == get_test_id_by_question_id(question_id))
            .one()
        )
        return test


def get_test_id_by_question_id(question_id: int) -> int:
    """
    Получение id теста по id вопроса.

    Args:
        question_id:
            id вопроса

    Returns:
        id теста
    """
    with Session() as session:
        test_id = (
            session.query(Question)
            .filter(Question.id == question_id)
            .one()
            .test_id
        )
        return test_id


def get_statistics_by_test_id(test_id: int) -> dict[str, int]:
    """
    Получение статистики по тесту.

    Args:
        test_id:
            id теста

    Returns:
        Словарь со статистикой
    """
    with Session() as session:
        results = session.query(Result).filter(Result.test_id == test_id)

        total = results.count()
        completed = results.filter(Result.score >= config.pass_score).count()

        statistics = {"total": total, "completed": completed}

        return statistics


def create_question(
    test_id: int, text: str, answers: dict[str, bool], image: str | None = None
) -> None:
    """
    Создание вопроса с ответами в базе данных.

    Args:
        test_id:
            id теста
        text:
            Текст вопроса
        answers:
            Словарь с ответами
        image:
            Ссылка на изображение (по умолчанию None)
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


def get_question_by_id(question_id: int) -> Question:
    """
    Получение вопроса по id.

    Args:
        question_id:
            id вопроса

    Returns:
        Вопрос
    """
    with Session() as session:
        question = (
            session.query(Question).filter(Question.id == question_id).one()
        )
        answers = (
            session.query(Answer)
            .filter(Answer.question_id == question.id)
            .all()
        )
        return question, answers


def get_questions_by_test_id(test_id: int) -> list[Question]:
    """
    Получение вопросов по id теста.

    Args:
        test_id:
            id теста

    Returns:
        Список вопросов
    """
    with Session() as session:
        questions = (
            session.query(Question).filter(Question.test_id == test_id).all()
        )
        return questions


def delete_question_by_id(question_id: int) -> None:
    """
    Удаление вопроса по id.

    Args:
        question_id:
            id вопроса
    """
    with Session() as session:
        session.query(Answer).filter(
            Answer.question_id == question_id
        ).delete()
        session.query(Question).filter(Question.id == question_id).delete()
        session.commit()


def change_correct_answer(
    question_id: int,
    answer_id: int,
) -> None:
    """
    Изменение правильного ответа.

    Args:
        question_id:
            id вопроса
        answer_id:
            id ответа
    """
    with Session() as session:
        session.query(Answer).filter(Answer.question_id == question_id).update(
            {"is_correct": False}
        )
        session.query(Answer).filter(Answer.id == answer_id).update(
            {"is_correct": True}
        )
        session.commit()


def get_users() -> list[User]:
    """
    Получение всех пользователей из базы данных.

    Returns:
        Список пользователей
    """
    with Session() as session:
        users = session.query(User).all()
        return users


def get_user_by_id(user_id: int) -> User:
    """
    Получение пользователя по id.

    Args:
        user_id:
            id пользователя

    Returns:
        Пользователь
    """
    with Session() as session:
        user = session.query(User).filter(User.id == user_id).one()
        return user


def get_count_results_by_user_id(user_id: int) -> dict[str, int]:
    """
    Получение результатов пользователя по id.

    Args:
        user_id:
            id пользователя

    Returns:
        Словарь с результатами
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


def get_results_by_user_id(user_id: int) -> list[Result]:
    """
    Получение результатов пользователя по id.

    Args:
        user_id:
            id пользователя

    Returns:
        Список результатов
    """
    with Session() as session:
        results = (
            session.query(Result)
            .filter(Result.user_id == user_id)
            .order_by(Result.id.desc())
            .all()
        )
        return results


def get_result_by_id(result_id: int) -> Result:
    """
    Получение результата по id.

    Args:
        result_id:
            id результата

    Returns:
        Результат
    """
    with Session() as session:
        result = session.query(Result).filter(Result.id == result_id).one()
        return result


def get_result_data_by_result(result: Result) -> list[tuple[str, str, str]]:
    """
    Получение данных результата.

    Args:
        result:
            Результат

    Returns:
        Данные результата
    """
    with Session() as session:
        q = aliased(Question)
        ia = aliased(IncorrectAnswer)
        a_user = aliased(Answer)
        a_correct = aliased(Answer)

        data = (
            session.query(
                q.text,
                a_correct.text,
                a_user.text,
            )
            .join(ia, ia.question_id == q.id)
            .join(a_user, a_user.id == ia.answer_id)
            .join(a_correct, a_correct.question_id == q.id)
            .filter(a_correct.is_correct, Result.id == result.id)
            .filter(ia.result_id == result.id)
            .all()
        )
        return data
