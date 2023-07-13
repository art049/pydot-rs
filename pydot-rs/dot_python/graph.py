from dataclasses import dataclass


@dataclass
class Graph:
    graph_name: str | None
    nodes: list[str]
    adjacency: dict[int, list[int]]
