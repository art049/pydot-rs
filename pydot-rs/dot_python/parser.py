from collections import defaultdict
from enum import Enum, auto
from typing import Iterable

from .tokenizer import Token, BasicToken, IdentifierToken
from .graph import Graph


class ParserState(Enum):
    Start = auto()
    ExpectGraphName = auto()
    ExpectLBracket = auto()
    ExpectNodeName = auto()
    ExpectEdgeOrSemicolon = auto()
    ExpectNodeNameOrRBracket = auto()
    End = auto()


class Parser:
    def __init__(self):
        self.state = ParserState.Start
        self.node_map: dict[str, int] = {}
        self.current_chain: list[int] = []

        self.graph_name: str | None = None
        self.nodes: list[str] = []
        self.adjacency: defaultdict[int, list[int]] = defaultdict(list)

    def get_node_index(self, name: str) -> int:
        """Get the index of a node, creating it if it doesn't exist"""
        node_idx = self.node_map.get(name, None)
        if node_idx is not None:
            return node_idx
        node_idx = len(self.nodes)
        self.nodes.append(name)
        return node_idx

    def persist_current_chain(self):
        """Persist the current chain of nodes as a path in the graph"""
        for i in range(len(self.current_chain) - 1):
            self.adjacency[self.current_chain[i]].append(self.current_chain[i + 1])
        self.current_chain = []

    def parse(self, tokens: Iterable[Token]) -> Graph:
        """Parse a list of tokens into a graph instance"""
        token_iter = iter(tokens)
        while self.state != ParserState.End:
            token = next(token_iter)
            self.parse_token(token)
        return Graph(
            graph_name=self.graph_name,
            nodes=self.nodes,
            adjacency=dict(self.adjacency),
        )

    def parse_token(self, token: Token):
        """Parse a single token"""
        match (self.state, token):
            # Graph header (type, name, bracket)
            case (ParserState.Start, BasicToken.GRAPH):
                self.state = ParserState.ExpectGraphName
            case (ParserState.ExpectGraphName, IdentifierToken(name)):
                self.graph_name = name
                self.state = ParserState.ExpectLBracket
            case (ParserState.ExpectLBracket, BasicToken.LEFT_BRACKET):
                self.state = ParserState.ExpectNodeNameOrRBracket

            # Graph body (nodes and edges)
            case (
                ParserState.ExpectNodeNameOrRBracket | ParserState.ExpectNodeName,
                IdentifierToken(name),
            ):
                node_idx = self.get_node_index(name)
                self.current_chain.append(node_idx)
                self.state = ParserState.ExpectEdgeOrSemicolon

            case (
                ParserState.ExpectEdgeOrSemicolon,
                BasicToken.EDGE,
            ):
                self.state = ParserState.ExpectNodeName

            case (ParserState.ExpectEdgeOrSemicolon, BasicToken.SEMICOLON):
                self.persist_current_chain()
                self.state = ParserState.ExpectNodeNameOrRBracket

            # Graph end (right bracket)
            case (ParserState.ExpectNodeNameOrRBracket, BasicToken.RIGHT_BRACKET):
                self.state = ParserState.End

            # Error cases (unexpected tokens)
            case _:
                raise Exception(f"Unexpected token {token} in state {self.state}")
