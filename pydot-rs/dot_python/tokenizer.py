from dataclasses import dataclass
from enum import Enum, auto
import re
from typing import Iterable


class BasicToken(Enum):
    GRAPH = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    SEMICOLON = auto()
    EDGE = auto()


@dataclass
class IdentifierToken:
    name: str


Token = BasicToken | IdentifierToken


def word_to_token(word: str) -> Token:
    match word:
        case "graph":
            return BasicToken.GRAPH
        case "{":
            return BasicToken.LEFT_BRACKET
        case "}":
            return BasicToken.RIGHT_BRACKET
        case ";":
            return BasicToken.SEMICOLON
        case "--":
            return BasicToken.EDGE
        case _:
            return IdentifierToken(word)


def tokenize(text: str) -> Iterable[Token]:
    words = (w for w in re.split(r"\s+|(\;)", text) if w is not None and w != "")
    return (word_to_token(w) for w in words)
