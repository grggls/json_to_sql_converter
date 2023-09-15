import json
from .nodes import InputNode, FilterNode, SortNode, TextTransformationNode, OutputNode
from .edges import create_graph_from_edges


def main(json_data):
    # Parse JSON data
    data = json.loads(json_data)

    # Extract nodes and edges
    edges = data.get("edges", [])
    nodes = data.get("nodes", [])

    # Create a dictionary to map edges to edge objects

    # Create a dictionary to map node types to their constructor functions
    node_type_to_constructor = {
        "INPUT": InputNode,
        "FILTER": FilterNode,
        "SORT": SortNode,
        "TEXT_TRANSFORMATION": TextTransformationNode,
        "OUTPUT": OutputNode,
    }

    node_objects = []

    # Create Node objects based on their type using the dictionary mapping
    for node_data in nodes:
        key = node_data["key"]
        node_type = node_data["type"]
        transform_object = node_data["transformObject"]

        # Use the switch statement to create the appropriate Node object
        if node_type in node_type_to_constructor:
            constructor = node_type_to_constructor[node_type]
            node_objects.append(constructor(key, node_type, transform_object))
        else:
            # Handle unsupported node types here
            print(f"Unsupported node type: {node_type}")

    # Print the list of Node objects
    for node in node_objects:
        print(f"Key: {node.key}, Type: {node.node_type}")
        print(f"Transform Object: {node.transform_object}")
        print()

    edges_graph = create_graph_from_edges(edges)

    # TODO
    for edge in edges_graph:
        print(edge)


if __name__ == "__main__":
    file_path = "../test/test-data/request-data.json"
    with open(file_path, "r") as file:
        json_data = file.read()

    main(json_data)
