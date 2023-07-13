from dataclasses import dataclass
from .tokenizer import tokenize
from .parser import Parser
from .graph import Graph


def parse_file(filepath: str) -> Graph:
    with open(filepath, "r") as f:
        text = f.read()
    tokens = tokenize(text)
    parser = Parser()
    graph = parser.parse(tokens)
    return graph


__all__ = ["parse_file", "Graph"]
