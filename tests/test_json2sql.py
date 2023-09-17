# ./tests/test_nodes.py
from json2sql import generate_query
from pathlib import Path
import unittest


class TestMainFunction(unittest.TestCase):
    def test_main_with_json_data(self):
        path = Path(__file__).parent / "test_data" / "request-data.json"
        with open(path, "r") as file:
            json_data = file.read()

        result = generate_query(json_data)

        # Read the expected SQL result from the "provided-result.sql" file
        path = Path(__file__).parent / "test_data" / "provided-result.sql"
        with open(path, "r") as file:
            expected_result = file.read()

        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
