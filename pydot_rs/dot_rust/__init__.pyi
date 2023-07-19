class Graph:
    graph_name: str | None
    nodes: list[str]
    adjacency: dict[int, list[int]]

def parse_file(filepath: str) -> Graph: ...
