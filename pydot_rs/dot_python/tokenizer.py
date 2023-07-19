from dataclasses import dataclass
from enum import Enum, auto
import re
from typing import Iterable


class BasicToken(Enum):
    Graph = auto()
    LeftBracket = auto()
    RightBracket = auto()
    Semicolon = auto()
    Edge = auto()


@dataclass
class IdentifierToken:
    name: str


Token = BasicToken | IdentifierToken


def word_to_token(word: str) -> Token:
    match word:
        case "graph":
            return BasicToken.Graph
        case "{":
            return BasicToken.LeftBracket
        case "}":
            return BasicToken.RightBracket
        case ";":
            return BasicToken.Semicolon
        case "--":
            return BasicToken.Edge
        case _:
            return IdentifierToken(word)


def tokenize(text: str) -> Iterable[Token]:
    words = (w for w in re.split(r"\s+|(\;)", text) if w is not None and w != "")
    return (word_to_token(w) for w in words)
