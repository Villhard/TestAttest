import unittest
from sqlalchemy import create_engine, inspect
from database.database import Base

from config import config


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(config.database.url)
        Base.metadata.create_all(self.engine)
        self.inspector = inspect(self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def given_tables_exist(self, tables):
        actual_tables = self.inspector.get_table_names()
        for table in tables:
            self.assertIn(table, actual_tables)

    def given_fields_exist(self, table, fields):
        actual_fields = self.inspector.get_columns(table)
        actual_fields = [col["name"] for col in actual_fields]
        for field in fields:
            self.assertIn(field, actual_fields)

    def test_check_tables_in_database(self):
        self.given_tables_exist(
            [
                "users",
                "tests",
                "questions",
                "answers",
                "results",
                "incorrect_answers",
            ]
        )

    def test_check_fields_in_users(self):
        self.given_fields_exist("users", ["id", "tg_id", "name", "surname"])

    def test_check_fields_in_tests(self):
        self.given_fields_exist(
            "tests", ["id", "title", "description", "is_publish"]
        )

    def test_check_fields_in_questions(self):
        self.given_fields_exist(
            "questions", ["id", "test_id", "text", "image"]
        )

    def test_check_fields_in_answers(self):
        self.given_fields_exist(
            "answers", ["id", "question_id", "text", "is_correct"]
        )

    def test_check_fields_in_results(self):
        self.given_fields_exist(
            "results", ["id", "test_id", "user_id", "score"]
        )

    def test_check_fields_in_incorrect_answers(self):
        self.given_fields_exist(
            "incorrect_answers",
            ["id", "result_id", "question_id", "answer_id"],
        )


if __name__ == "__main__":
    unittest.main()
