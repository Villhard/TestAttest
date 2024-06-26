"""
Модуль для работы с базой данных для админа.

Содержит функции для создания, удаления, публикации тестов,
создания вопросов с ответами, получения статистики по тестам,
получения пользователей и их результатов.

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


def create_test(title: str, description: str) -> None:
    """Create test."""
    with Session() as session:
        test = Test(
            title=title,
            description=description,
        )
        session.add(test)
        session.commit()


def get_tests() -> list[Test]:
    with Session() as session:
        tests = session.query(Test).order_by(Test.id.desc()).all()
        return tests


def get_test_by_id(test_id: int) -> Test:
    """Get test by id."""
    with Session() as session:
        test = session.query(Test).filter(Test.id == test_id).one()
        return test


def delete_test_by_id(test_id: int) -> None:
    """Delete test by id."""
    with Session() as session:
        session.query(IncorrectAnswer).filter(
            IncorrectAnswer.result.has(test_id=test_id)
        ).delete()
        session.query(Result).filter(Result.test_id == test_id).delete()
        session.query(Answer).filter(Answer.question.has(test_id=test_id)).delete()
        session.query(Question).filter(Question.test_id == test_id).delete()
        session.query(Test).filter(Test.id == test_id).delete()
        session.commit()


def publish_test_by_id(test_id: int) -> None:
    """Publish test by id."""
    with Session() as session:
        session.query(Test).filter(Test.id == test_id).update({"is_publish": True})
        session.commit()


def get_test_by_question_id(question_id: int) -> Test:
    """Get test by question id."""
    with Session() as session:
        test = (
            session.query(Test)
            .filter(Test.id == get_test_id_by_question_id(question_id))
            .one()
        )
        return test


def get_test_id_by_question_id(question_id: int) -> int:
    """Get test id by question id."""
    with Session() as session:
        test_id = (
            session.query(Question).filter(Question.id == question_id).one().test_id
        )
        return test_id


def get_statistics_by_test_id(test_id: int) -> dict[str, int]:
    """Get statistics by test id."""
    with Session() as session:
        results = session.query(Result).filter(Result.test_id == test_id)

        total = results.count()
        completed = results.filter(Result.score >= config.pass_score).count()

        statistics = {
            "completed": completed,
            "total": total,
        }

        return statistics


def create_question(
    test_id: int, text: str, answers: dict[str, bool], image: str | None = None
) -> None:
    """Create question."""
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


def get_question_by_id(
    question_id: int,
) -> tuple[Question, list[Answer]]:
    """Get question and answers by question id."""
    with Session() as session:
        question = session.query(Question).filter(Question.id == question_id).one()
        answers = session.query(Answer).filter(Answer.question_id == question.id).all()
        return question, answers


def get_questions_by_test_id(test_id: int) -> list[Question]:
    """Get questions by test id."""
    with Session() as session:
        questions = session.query(Question).filter(Question.test_id == test_id).all()
        return questions


def delete_question_by_id(question_id: int) -> None:
    """Delete question by id."""
    with Session() as session:
        session.query(Answer).filter(Answer.question_id == question_id).delete()
        session.query(Question).filter(Question.id == question_id).delete()
        session.commit()


def change_correct_answer(
    question_id: int,
    answer_id: int,
) -> None:
    """Change correct answer."""
    with Session() as session:
        session.query(Answer).filter(Answer.question_id == question_id).update(
            {"is_correct": False}
        )
        session.query(Answer).filter(Answer.id == answer_id).update(
            {"is_correct": True}
        )
        session.commit()


def get_users() -> list[User]:
    """Get all users."""
    with Session() as session:
        users = session.query(User).all()
        return users


def get_user_by_id(user_id: int) -> User:
    """Get user by id."""
    with Session() as session:
        user = session.query(User).filter(User.id == user_id).one()
        return user


def get_count_results_by_user_id(user_id: int) -> dict[str, int]:
    """Get dictionary of completed and total tests for user."""
    with Session() as session:
        total_tests = session.query(Test).count()
        completed_tests = (
            session.query(Result)
            .filter(Result.user_id == user_id)
            .group_by(Result.test_id)
            .filter(Result.score >= config.pass_score)
            .count()
        )
        return {"completed": completed_tests, "total": total_tests}


def get_results_by_user_id(user_id: int) -> list[Result]:
    """Get list of results for user."""
    with Session() as session:
        results = (
            session.query(Result)
            .filter(Result.user_id == user_id)
            .order_by(Result.id.desc())
            .all()
        )
        return results


def get_result_by_id(result_id: int) -> Result:
    """Get result by id."""
    with Session() as session:
        result = session.query(Result).filter(Result.id == result_id).one()
        return result


def get_result_data_by_result(result: Result) -> list[tuple[str, str, str]]:
    """Get data of result."""
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
