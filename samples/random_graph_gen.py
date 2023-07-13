import random


def generate_random_graph(num_nodes, connexity):
    # Ensure connexity is within an acceptable range
    if connexity < 0 or connexity > 1:
        raise ValueError("Connexity must be between 0 and 1")

    # Begin the graph definition
    graph_def = "graph graphname {\n"

    # Create a list of nodes
    nodes = [str(i) for i in range(num_nodes)]

    # Determine the number of edges based on connexity
    num_edges = int(
        connexity * (num_nodes * (num_nodes - 1) // 2)
    )  # maximum number of edges in a graph is n(n - 1) / 2

    # Create a set to hold unique edges
    edges = set()

    while len(edges) < num_edges:
        # Pick two different nodes at random
        n1, n2 = random.sample(nodes, 2)

        # Create an edge. Use a tuple with sorted nodes to prevent duplicate edges in the opposite direction
        edge = tuple(sorted((n1, n2)))

        # Add the edge to the set of edges (duplicates will be ignored automatically)
        edges.add(edge)

    # Add edges to the graph definition
    for edge in edges:
        graph_def += f"    {edge[0]} -- {edge[1]};\n"

    # Close the graph definition
    graph_def += "}\n"

    return graph_def


# Use the function to create a random graph and write it to a file
graph = generate_random_graph(1000, 0.1)
with open("graph.dot", "w") as f:
    f.write(graph)
