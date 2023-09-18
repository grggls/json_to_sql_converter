import json
from .nodes import InputNode, FilterNode, SortNode, TextTransformationNode, OutputNode
from .edges import create_graph_from_edges
from .validate_json import validate_json
from .validate_sql import validate_sql


def generate_query(text_data):
    # validate incoming data and parse into JSON
    json_data = json.loads(text_data)
    validate_json(json_data)

    # Extract nodes and edges
    edges = json_data.get("edges", [])
    nodes = json_data.get("nodes", [])

    # Create a dictionary to map edges to edge objects
    edges_graph = create_graph_from_edges(edges)

    # Create a dictionary to map node types to their constructor functions
    node_type_to_constructor = {
        "INPUT": InputNode,
        "FILTER": FilterNode,
        "SORT": SortNode,
        "TEXT_TRANSFORMATION": TextTransformationNode,
        "OUTPUT": OutputNode,
    }

    node_objects = {}

    # Create Node objects based on their type using the dictionary mapping
    for node_data in nodes:
        key = node_data["key"]
        node_type = node_data["type"]
        transform_object = node_data["transformObject"]

        # use the node type constructor dictionary to call the correct constructor
        if node_type in node_type_to_constructor:
            constructor = node_type_to_constructor[node_type]
            node_objects[key] = constructor(key, node_type, transform_object)
        else:
            # Handle unsupported node types here
            print(f"Unsupported node type: {node_type}")

    # Create a list of nodes ordered according to their edges
    nodes = depth_first_search(edges_graph)

    # start to formulate the query
    query_string = (
        "-- Create a temporary table\nCREATE TEMP TABLE temp_result AS\nWITH "
    )

    # Skip the first element (nodes[0] = 0)
    next(nodes)

    # Get the input node and amend the query_string
    input_node = node_objects[next(nodes)]
    query_string += input_node.generate_sql()

    # For the next step in the query, the previous node key
    from_node_key = input_node.key

    # Get each subsequent node and continue to add to the query string
    for node in nodes:
        # Add the result of the node.generate_sql() method to the query string
        query_string += node_objects[node].generate_sql(input_node, from_node_key)
        # Advance the from_node_key for the next iteration
        from_node_key = node_objects[node].key

    # The last bit of the query string returning all results we've input, sorted, etc.
    query_string += f"SELECT * FROM {from_node_key};"

    # verify that the sql is syntactically correct, at least
    validate_sql(query_string)

    # verify that we've created valid json
    return query_string


# take a dictionary of edges and a dictionary of nodes and formulate a sql query
def depth_first_search(edges):
    node = 0
    while node != "":
        yield node
        node = edges.get(node, "")


if __name__ == "__main__":
    file_path = "../test/test-data/request-data.json"
    with open(file_path, "r") as file:
        json_data = file.read()

    generate_query(json_data)
