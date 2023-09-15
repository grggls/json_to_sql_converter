class BaseNode:
    def __init__(self, key, node_type, transform_object):
        self.key = key
        self.node_type = node_type
        self.transform_object = transform_object

    def generate_sql(self):
        # Common logic here
        pass


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
# SELECT id, name, age FROM users
# Generate SQL SELECT statement based on transform_object
class InputNode(BaseNode):
    def generate_sql(self):
        # Extract tableName and fields from the transformObject
        table_name = self.transform_object.get("tableName", "")
        fields = self.transform_object.get("fields", [])

        if not table_name or not fields:
            # Handle missing or invalid data
            return ""

        # Build the SQL query string
        field_list = ", ".join(fields)
        return f"SELECT {field_list} FROM {table_name}"


# {
#     "key": "B",
#     "type": "FILTER",
#     "transformObject": {
#         "variable_field_name": "age",
#         "joinOperator": "AND",
#         "operations": [
#             {
#                 "operator": ">",
#                 "value": "18"
#             }
#         ]
#     }
# }
#
# --->
#
# SELECT `id`, `name`, `age` FROM `A` WHERE `age` > 18
# Generate SQL SELECT statement based on transform_object
class FilterNode(BaseNode):
    def generate_sql(self):
        # TODO: Extract tableName from Edges
        table_name = "A"
        # TODO: Extract fields from InputNode
        fields = self.transform_object.get("fields", [])

        if not table_name or not fields:
            # Handle missing or invalid data
            return ""

        # Build the SQL query string
        field_list = ", ".join(fields)
        return f"SELECT {field_list} FROM {table_name}"


class SortNode(BaseNode):
    def generate_sql(self):
        # TODO: generate SQL
        pass


class TextTransformationNode(BaseNode):
    def generate_sql(self):
        # TODO: generate SQL
        pass


class OutputNode(BaseNode):
    def generate_sql(self):
        # TODO: generate SQL
        pass
