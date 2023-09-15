# Create a dictionary representation of a graph of edges where each key is a 'from_node'
# and each value is a single 'to_node'.
#
# Graph dictionaries are linear, start with a 0 element, and end with an empty string
# value, i.e. graph[LAST NODE] = '', e.g.
#
#    {0:'A', 'A':'B', 'B':'C', 'C':'D', 'D':''}
#
# Assume two things: that the first edge in the JSON is the start of the graph, and that
# edges are added to the JSON object in somewhat sequential order
#
def create_graph_from_edges(edges):
    graph = {}

    for edge in edges:
        from_node, to_node = edge["from"], edge["to"]

        # If graph is empty, first add 0 node
        if not graph:
            graph[0] = from_node
            graph[from_node] = to_node
            graph[to_node] = ""
        else:
            # Detect circular graph (A -> B, B -> A) and break
            if to_node in graph and graph[to_node] != "":
                print("circular graph detected. ignoring this edge.")
                break

            # Detect branching graph (A -> B, A -> C) and break
            if from_node in graph and graph[from_node] != "":
                print("branching graph detected. ignoring.")
                break

            # Detect second, unlinked graph (A -> B, C -> D) and break
            if from_node not in graph:
                print("second graph detected. ignoring.")
                break

            else:
                # Add the edge
                graph[from_node] = to_node
                # Add the first half of the edge, or the last node in the graph
                graph[to_node] = ""

    return graph


if __name__ == "__main__":
    print(
        create_graph_from_edges(
            [
                {"from": "A", "to": "B"},
                {"from": "B", "to": "C"},
                {"from": "C", "to": "D"},
                {"from": "E", "to": "F"},
            ]
        )
    )
