use std::collections::HashMap;

use crate::{tokenizer::Token, Graph};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum ParserState {
    Start,
    ExpectGraphName,
    ExpectLBracket,
    ExpectNodeName,
    ExpectEdgeOrSemicolon,
    ExpectNodeNameOrRBracket,
    End,
}

pub struct Parser {
    state: ParserState,
    node_map: HashMap<String, usize>,
    current_chain: Vec<usize>,

    graph_name: String,
    nodes: Vec<String>,
    adjacency: HashMap<usize, Vec<usize>>,
}

impl Parser {
    pub fn new() -> Self {
        Self {
            state: ParserState::Start,
            node_map: HashMap::new(),
            current_chain: Vec::new(),

            graph_name: String::new(),
            nodes: Vec::new(),
            adjacency: HashMap::new(),
        }
    }

    /// Get the index of a node, or insert it if it doesn't exist.
    fn get_node_index(&mut self, name: &str) -> usize {
        *self.node_map.entry(name.to_string()).or_insert_with(|| {
            let index = self.nodes.len();
            self.nodes.push(name.to_string());
            self.adjacency.insert(index, Vec::new());
            index
        })
    }

    /// Persist the current chain of nodes as a path in the graph
    fn persist_current_chain(&mut self) {
        for i in 0..self.current_chain.len() - 1 {
            self.adjacency
                .get_mut(&self.current_chain[i])
                .unwrap()
                .push(self.current_chain[i + 1]);
        }
        self.current_chain.clear();
    }

    pub fn parse(&mut self, tokens: &mut impl Iterator<Item = Token>) -> Graph {
        while self.state != ParserState::End {
            let token = tokens.next().unwrap();
            self.parse_token(token);
        }
        Graph {
            graph_name: self.graph_name.clone(),
            nodes: self.nodes.clone(),
            adjacency: self.adjacency.clone(),
        }
    }

    /// Parse a single token
    fn parse_token(&mut self, token: Token) {
        match (self.state, token) {
            // Graph header (type, name, bracket)
            (ParserState::Start, Token::Graph) => {
                self.state = ParserState::ExpectGraphName;
            }
            (ParserState::ExpectGraphName, Token::Identifier(name)) => {
                self.graph_name = name;
                self.state = ParserState::ExpectLBracket;
            }
            (ParserState::ExpectLBracket, Token::LeftBracket) => {
                self.state = ParserState::ExpectNodeName;
            }

            // Graph Body
            (
                ParserState::ExpectNodeNameOrRBracket | ParserState::ExpectNodeName,
                Token::Identifier(name),
            ) => {
                let index = self.get_node_index(&name);
                self.current_chain.push(index);
                self.state = ParserState::ExpectEdgeOrSemicolon;
            }
            (ParserState::ExpectEdgeOrSemicolon, Token::UndirectedEdgeOp) => {
                self.state = ParserState::ExpectNodeName;
            }
            (ParserState::ExpectEdgeOrSemicolon, Token::Semicolon) => {
                self.persist_current_chain();
                self.state = ParserState::ExpectNodeNameOrRBracket;
            }

            // Graph End
            (ParserState::ExpectNodeNameOrRBracket, Token::RightBracket) => {
                self.state = ParserState::End;
            }

            // Error
            (state, token) => {
                panic!("Unexpected token {:?} in state {:?}", token, state);
            }
        }
    }
}
