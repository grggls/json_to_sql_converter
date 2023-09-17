import re


class BaseNode:
    def __init__(self, key, node_type, transform_object):
        self.key = key
        self.node_type = node_type
        self.transform_object = transform_object

    def generate_sql(self):
        return f"Node(key={self.key}, type={self.node_type}, transform_object={self.transform_object})"


# {
#    "key": "A",
#    "type": "INPUT",
#    "transformObject": {
#        "tableName": "users",
#        "fields": [
#            "id",
#            "name",
#            "age"
#        ]
#    }
# }
#
# --->
#
# A as (
#    SELECT `id`, `name`, `age` FROM `users`
# )
class InputNode(BaseNode):
    def generate_sql(self):
        # Extract tableName and fields from the transformObject
        table_name = self.transform_object.get("tableName", "")
        fields = self.transform_object.get("fields", [])

        if not table_name or not fields:
            # Handle missing or invalid data
            return ""

        # Build the SQL query string
        formatted_fields = [f"`{field}`" for field in fields]
        self.field_list = ", ".join(formatted_fields)
        return (
            f"{self.key} as (\n    SELECT {self.field_list} FROM `{table_name}`\n),\n"
        )


# "key": "B",
# "type": "FILTER",
# "transformObject": {
#     "variable_field_name": "age",
#     "joinOperator": "AND",
#     "operations": [
#         {
#         "operator": ">",
#         "value": "18"
#         }
#     ]
# }
# --->
# B as (
#    SELECT `id`, `name`, `age` FROM `A` WHERE `age` > 18
# ),
class FilterNode(BaseNode):
    def generate_sql(self, input_node: InputNode, from_node_key: str):
        # TODO: account for additional joinOperators
        variable_field_name = self.transform_object.get("variable_field_name", "")
        operations = self.transform_object.get("operations", [])
        # Extract the operations
        filter = " ".join(
            [
                f"{operation.get('operator', '')} {operation.get('value', '')}"
                for operation in operations
            ]
        )
        return f"{self.key} as (\n    SELECT {input_node.field_list} FROM `{from_node_key}` WHERE `{variable_field_name}` {filter}\n),\n"


# {
#    "key": "C",
#    "type": "SORT",
#    "transformObject": [
#       {
#            "target": "age",
#            "order": "ASC"
#        },
#        {
#            "target": "name",
#            "order": "ASC"
#        }
#    ]
# }
#
# --->
#
# C as (
#    SELECT `id`, `name`, `age` FROM `B` ORDER BY `age`, `name` DESC
# ),
class SortNode(BaseNode):
    def generate_sql(self, input_node: InputNode, from_node: str):
        # TODO: account for different orders
        targets = ", ".join([f"`{item['target']}`" for item in self.transform_object])
        return f"{self.key} as (\n    SELECT {input_node.field_list} FROM `{from_node}` ORDER BY {targets} DESC\n),\n"


# {
#    "key": "D",
#    "type": "TEXT_TRANSFORMATION",
#    "transformObject": [
#        {
#            "column": "name",
#            "transformation": "UPPER"
#        }
#    ]
# }
#
# --->
#
# D as (
#    SELECT `id`, UPPER(`name`) as `name`, `age` FROM `C`
# )
class TextTransformationNode(BaseNode):
    def generate_sql(self, input_node: InputNode, from_node: str):
        # Extract fields from the input_node.field list with a regular expression looking for backticks
        fields = re.findall(r"(`.*?`)", input_node.field_list)

        transformed_fields = []

        # for each field in the original input statement
        for field in fields:
            # for each transformObject ruleset
            for rule in self.transform_object:
                # if field matches, apply the transform
                if f"`{rule['column']}`" == field:
                    transformed_field = f"{rule['transformation']}({field}) as {field}"
                    break
            else:
                # If no matching rule is found, use the original field
                transformed_field = field

            transformed_fields.append(transformed_field)

        return f"{self.key} as (\n    SELECT {', '.join(transformed_fields)} FROM `{from_node}`\n),\n"


# {
#    "key": "E",
#    "type": "OUTPUT",
#    "transformObject": {
#        "limit": 100,
#        "offset": 0
#    }
# }
#
# --->
#
# E as (
#    SELECT * FROM `D` limit 100 offset 0
# )
class OutputNode(BaseNode):
    def generate_sql(self, input_node: InputNode, from_node: str):
        return f"{self.key} as (\n    SELECT * FROM `{from_node}` limit {self.transform_object.get('limit', '')} offset 0\n)\n"
