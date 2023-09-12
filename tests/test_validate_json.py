from json2sql.validate_json import validate_json
from pathlib import Path
import unittest
import json


class TestValidateJSON(unittest.TestCase):
    # loads and validates request-data.json against the schema
    def test_valid_json(self):
        path = Path(__file__).parent / "test_data" / "request-data.json"
        with open(path, "r") as f:
            data = json.load(f)

        self.assertTrue(validate_json(data))

    # nodes without edges
    def test_missing_edges(self):
        data = {
            "nodes": [
                {
                    "key": "A",
                    "type": "INPUT",
                    "transformObject": {
                        "tableName": "users",
                        "fields": ["id", "name", "age"],
                    },
                }
            ]
        }
        self.assertFalse(validate_json(data))

    # edges without nodes
    def test_missing_nodes(self):
        data = {
            "edges": [
                {"from": "A", "to": "B"},
                {"from": "B", "to": "C"},
                {"from": "C", "to": "D"},
                {"from": "D", "to": "E"},
            ]
        }
        self.assertFalse(validate_json(data))


if __name__ == "__main__":
    unittest.main()
