from collections import defaultdict
from dataclasses import dataclass
import sys
from enum import Enum, auto
import re
from itertools import dropwhile, takewhile


class BasicToken(Enum):
    GRAPH = auto()
    DIGRAPH = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    SEMICOLON = auto()
    DIRECTED_EDGE_OP = auto()
    UNDIRECTED_EDGE_OP = auto()


@dataclass
class IdentifierToken:
    name: str


Token = BasicToken | IdentifierToken


def word_to_token(word: str) -> Token:
    match word:
        case "graph":
            return BasicToken.GRAPH
        case "digraph":
            return BasicToken.DIGRAPH
        case "{":
            return BasicToken.LEFT_BRACKET
        case "}":
            return BasicToken.RIGHT_BRACKET
        case ";":
            return BasicToken.SEMICOLON
        case "->":
            return BasicToken.DIRECTED_EDGE_OP
        case "--":
            return BasicToken.UNDIRECTED_EDGE_OP
        case _:
            return IdentifierToken(word)


def tokenize(text: str) -> list[Token]:
    words = (w for w in re.split(r"\s+|(\;)", text) if w is not None and w != "")
    return [word_to_token(w) for w in words]


@dataclass
class Graph:
    is_directed: bool
    nodes: list[str]
    adjacency: dict[int, list[int]]


def parse_file(filepath: str) -> Graph:
    with open(filepath, "r") as f:
        text = f.read()
        tokens = tokenize(text)
    token_iter = iter(tokens)
    first_token = next(token_iter)
    if first_token == BasicToken.GRAPH:
        is_directed = False
    elif first_token == BasicToken.DIGRAPH:
        is_directed = True
    else:
        raise Exception("Expected graph or digraph")
    token_iter = dropwhile(lambda t: t != BasicToken.LEFT_BRACKET, token_iter)
    next(token_iter)  # Skip left bracket
    graph_tokens = takewhile(lambda t: t != BasicToken.RIGHT_BRACKET, token_iter)
    nodes: list[str] = []
    adjacency = defaultdict(list)
    node_map: dict[str, int] = {}
    id_buffer: list[int] = []
    for t in graph_tokens:
        match t:
            case IdentifierToken(name):
                index = node_map.get(name, None)
                if index is None:
                    index = len(nodes)
                    nodes.append(name)
                    node_map[name] = index
                id_buffer.append(index)
            case BasicToken.DIRECTED_EDGE_OP:
                if not is_directed:
                    raise Exception("Unexpected directed edge operator")
            case BasicToken.UNDIRECTED_EDGE_OP:
                if is_directed:
                    raise Exception("Unexpected undirected edge operator")
            case BasicToken.SEMICOLON:
                if is_directed:
                    for i in range(len(id_buffer) - 1):
                        adjacency[id_buffer[i]].append(id_buffer[i + 1])
                else:
                    for i in range(len(id_buffer) - 1):
                        adjacency[id_buffer[i]].append(id_buffer[i + 1])
                        adjacency[id_buffer[i + 1]].append(id_buffer[i])
                id_buffer = []
            case other:
                raise Exception(f"Unexpected token {other}")

    if next(token_iter, None) is not None:
        raise Exception("Unexpected token after right bracket")

    return Graph(is_directed, nodes, dict(adjacency))


if __name__ == "__main__":
    graph = parse_file(sys.argv[1])
    print(graph)
