from jsonschema import validate, ValidationError


def validate_json(data):
    # Define our schema
    schema = {
        "type": "object",
        "properties": {
            "nodes": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "key": {"type": "string"},
                        "type": {
                            "type": "string",
                            "enum": [
                                "INPUT",
                                "FILTER",
                                "SORT",
                                "TEXT_TRANSFORMATION",
                                "OUTPUT",
                            ],
                        },  # noqa: E501
                        "transformObject": {
                            "oneOf": [
                                {
                                    "type": "object",
                                    "properties": {
                                        "tableName": {"type": "string"},
                                        "fields": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                        },  # noqa: E501
                                    },
                                    "required": ["tableName", "fields"],
                                },
                                {
                                    "type": "object",
                                    "properties": {
                                        "variable_field_name": {"type": "string"},
                                        "joinOperator": {"type": "string"},
                                        "operations": {
                                            "type": "array",
                                            "items": {"type": "object"},
                                        },  # noqa: E501
                                    },
                                    "required": [
                                        "variable_field_name",
                                        "joinOperator",
                                        "operations",
                                    ],  # noqa: E501
                                },
                                {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "target": {"type": "string"},
                                            "order": {
                                                "type": "string",
                                                "enum": ["ASC", "DESC"],
                                            },  # noqa: E501
                                        },
                                        "required": ["target", "order"],
                                    },
                                },
                                {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "column": {"type": "string"},
                                            "transformation": {"type": "string"},
                                        },
                                        "required": ["column", "transformation"],
                                    },
                                },
                                {
                                    "type": "object",
                                    "properties": {
                                        "limit": {"type": "integer"},
                                        "offset": {"type": "integer"},
                                    },
                                    "required": ["limit", "offset"],
                                },
                            ]
                        },
                    },
                    "required": ["key", "type", "transformObject"],
                },
            },
            "edges": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "from": {"type": "string"},
                        "to": {"type": "string"},
                    },
                    "required": ["from", "to"],
                },
            },
        },
        "required": ["nodes", "edges"],
    }

    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError as e:
        print(f"Validation failed: {e.message}")
        return False
