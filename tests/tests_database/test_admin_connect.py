import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config
from database.admin_connect import (
    create_test,
    get_tests,
    get_test_by_id,
    delete_test_by_id,
)
from database.database import Base, Test


class TestAdminConnect(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(config.database.url)
        self.Session = sessionmaker(self.engine)

        Base.metadata.create_all(self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_create_test(self):
        # Given
        title = "test"
        description = "description"

        # When
        with self.Session() as session:
            create_test(
                title=title,
                description=description,
                session=session,
            )

        # Then
        with self.Session() as session:
            test = session.query(Test).filter(Test.id == 1).one()
            self.assertEqual(test.title, title)
            self.assertEqual(test.description, description)

    def test_get_tests(self):
        # Given
        test1 = Test(
            title="test1",
            description="description for test1",
        )
        test2 = Test(
            title="test2",
            description="description for test2",
        )

        with self.Session() as session:
            session.add_all([test1, test2])
            session.commit()

        # When
        with self.Session() as session:
            tests = get_tests(session)

        # Then
        self.assertEqual(len(tests), 2)
        self.assertTrue(
            any(
                test.title == "test1"
                and test.description == "description for test1"
                for test in tests
            )
        )
        self.assertTrue(
            any(
                test.title == "test2"
                and test.description == "description for test2"
                for test in tests
            )
        )

    def test_get_test_by_id(self):
        # Given
        test1 = Test(
            title="test1",
            description="description for test1",
        )
        test2 = Test(
            title="test2",
            description="description for test2",
        )

        with self.Session() as session:
            session.add_all([test1, test2])
            session.commit()

        # When
        with self.Session() as session:
            test1_query = get_test_by_id(1, session)
            test2_query = get_test_by_id(2, session)

        # Then
        self.assertEqual(test1_query.title, "test1")
        self.assertEqual(test1_query.description, "description for test1")
        self.assertEqual(test2_query.title, "test2")
        self.assertEqual(test2_query.description, "description for test2")

    def test_delete_test_by_id(self):
        # Given
        test1 = Test(
            title="test1",
            description="description for test1",
        )
        test2 = Test(
            title="test2",
            description="description for test2",
        )
        with self.Session() as session:
            session.add_all([test1, test2])
            session.commit()

        # When
        with self.Session() as session:
            delete_test_by_id(1, session)

        # Then
        with self.Session() as session:
            tests = session.query(Test).all()
            self.assertEqual(len(tests), 1)
            with self.assertRaises(Exception) as error:
                get_test_by_id(1, session)
                self.assertEqual(
                    str(error.exception),
                    "sqlalchemy.exc.NoResultFound: No row was found when one was required",
                )

    def test_publish_test_by_id(self):
        pass

    def test_get_questions_by_test_id(self):
        pass

    def test_create_question(self):
        pass

    def test_get_statistics_by_test_id(self):
        pass

    def test_get_users(self):
        pass

    def test_get_user_by_id(self):
        pass

    def test_get_count_results_by_user_id(self):
        pass

    def test_get_question_by_id(self):
        pass

    def test_change_correct_answer(self):
        pass

    def test_get_test_id_by_question_id(self):
        pass

    def test_get_test_by_question_id(self):
        pass

    def test_delete_question_by_id(self):
        pass

    def test_get_results_by_user_id(self):
        pass

    def test_get_result_by_id(self):
        pass

    def test_get_result_data_by_result(self):
        pass


if __name__ == "__main__":
    unittest.main()
