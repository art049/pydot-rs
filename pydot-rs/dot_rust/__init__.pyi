class Graph:
    is_directed: bool
    nodes: list[str]
    adjacency: list[list[int]]

def parse_file(filepath: str) -> Graph: ...
