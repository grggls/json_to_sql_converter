from pathlib import Path
import unittest
import sqlite3


class TestValidateSQL(unittest.TestCase):
    # Initialize an in-memory SQLite database
    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(":memory:")
        cls.cursor = cls.conn.cursor()
        cls.apply_sql_schema()

    @classmethod
    def apply_sql_schema(cls):
        path = Path(__file__).parent / "test_data" / "schema.sql"
        with open(path, "r") as f:
            sql_schema = f.read()
        cls.cursor.executescript(sql_schema)

    # Clean up the database
    @classmethod
    def tearDownClass(cls):
        # Close the connection
        cls.conn.close()

    def test_apply_test_data(self):
        # load the test data
        path = Path(__file__).parent / "test_data" / "test-data.sql"
        with open(path, "r") as f:
            sql_data = f.read()
        try:
            self.cursor.executescript(sql_data)
        except sqlite3.Error as e:
            self.fail(f"SQL test data is invalid: {e}")

    def test_query_data_with_dummy_result(self):
        # load the schema
        path = Path(__file__).parent / "test_data" / "dummy-result.sql"
        with open(path, "r") as f:
            sql_data = f.read()
        try:
            self.cursor.executescript(sql_data)
        except sqlite3.Error as e:
            self.fail(f"File dummy-result.sql is invalid: {e}")

        # Now, let's fetch the results and print them
        self.cursor.execute("SELECT * FROM temp_result")

        rows = self.cursor.fetchall()
        for row in rows[:10]:
            print(row)


if __name__ == "__main__":
    unittest.main()
