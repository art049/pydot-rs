use std::collections::HashMap;

use anyhow::{anyhow, bail};
use pyo3::{exceptions::PyValueError, prelude::*};
use regex::Regex;

#[derive(Debug, Clone, PartialEq, Eq)]
enum Token {
    Graph,
    Digraph,
    LeftBracket,
    RightBracket,
    Semicolon,
    DirectedEdgeOp,
    UndirectedEdgeOp,
    Identifier(String),
}

fn word_to_token(word: &str) -> Token {
    match word {
        "graph" => Token::Graph,
        "digraph" => Token::Digraph,
        "{" => Token::LeftBracket,
        "}" => Token::RightBracket,
        ";" => Token::Semicolon,
        "->" => Token::DirectedEdgeOp,
        "--" => Token::UndirectedEdgeOp,
        _ => Token::Identifier(word.to_string()),
    }
}

fn split_words(text: &str) -> Vec<&str> {
    let re = Regex::new(r"(\s+|;)").unwrap();
    let mut words: Vec<&str> = Vec::new();
    let mut prev_end = 0;

    for mat in re.find_iter(text) {
        let (start, end) = (mat.start(), mat.end());

        if start != prev_end {
            words.push(&text[prev_end..start]);
        }
        if text[start..end].trim() != "" {
            words.push(&text[start..end]);
        }
        prev_end = end;
    }

    if prev_end != text.len() {
        words.push(&text[prev_end..]);
    }

    words
}

#[cfg(test)]
mod test {
    use super::*;
    use insta::assert_debug_snapshot;

    #[test]
    fn test_split() {
        let text = "This is an;example of text;to   split";
        assert_debug_snapshot!(split_words(text), @r###"
        [
            "This",
            "is",
            "an",
            ";",
            "example",
            "of",
            "text",
            ";",
            "to",
            "split",
        ]
        "###);
    }

    #[test]
    fn test_split_graph() {
        let text = "graph graphname {\n    a -- b -- c;\n    b -- d;\n}";
        assert_debug_snapshot!(split_words(text), @r###"
        [
            "graph",
            "graphname",
            "{",
            "a",
            "--",
            "b",
            "--",
            "c",
            ";",
            "b",
            "--",
            "d",
            ";",
            "}",
        ]
        "###);
    }

    #[test]
    fn test_split_digraph() {
        let filename = concat!(env!("CARGO_MANIFEST_DIR"), "/samples/dir.dot").to_string();
        assert_debug_snapshot!(parse_file(filename), @r###"
        Ok(
            Graph {
                is_directed: true,
                nodes: [
                    "a",
                    "b",
                    "c",
                    "d",
                ],
                adjacency: [
                    [
                        1,
                    ],
                    [
                        2,
                        3,
                    ],
                    [],
                    [],
                ],
            },
        )
        "###);
    }
}

#[pyclass]
#[derive(Debug)]
struct Graph {
    pub is_directed: bool,
    pub nodes: Vec<String>,
    pub adjacency: Vec<Vec<usize>>,
}

#[pyfunction]
fn parse_file(filepath: String) -> PyResult<Graph> {
    let text = std::fs::read_to_string(filepath)?;
    let words = split_words(&text);
    let mut token_it = words.into_iter().map(word_to_token);
    let first_token = token_it
        .next()
        .ok_or_else(|| anyhow!("Expected graph or digraph"))?;
    let is_directed = match first_token {
        Token::Graph => false,
        Token::Digraph => true,
        _ => return Err(anyhow!("Expected graph or digraph").into()),
    };
    let mut token_it = token_it.skip_while(|t| *t != Token::LeftBracket);
    token_it.next(); // Skip left bracket
    let graph_tokens: Vec<Token> = token_it
        .by_ref()
        .take_while(|t| *t != Token::RightBracket)
        .collect();
    let mut nodes: Vec<String> = Vec::new();
    let mut adjacency: Vec<Vec<usize>> = Vec::new();
    let mut node_map: HashMap<String, usize> = HashMap::new();
    let mut id_buffer: Vec<usize> = Vec::new();
    for t in graph_tokens {
        match t {
            Token::Identifier(name) => {
                let index = *node_map.entry(name.clone()).or_insert_with(|| {
                    let index = nodes.len();
                    nodes.push(name);
                    adjacency.push(Vec::new());
                    index
                });
                id_buffer.push(index);
            }
            Token::DirectedEdgeOp => {
                if !is_directed {
                    return Err(anyhow!("Unexpected directed edge operator").into());
                }
            }
            Token::UndirectedEdgeOp => {
                if is_directed {
                    return Err(anyhow!("Unexpected undirected edge operator").into());
                }
            }
            Token::Semicolon => {
                if is_directed {
                    for i in 0..id_buffer.len() - 1 {
                        adjacency[id_buffer[i]].push(id_buffer[i + 1]);
                    }
                } else {
                    for i in 0..id_buffer.len() - 1 {
                        adjacency[id_buffer[i]].push(id_buffer[i + 1]);
                        adjacency[id_buffer[i + 1]].push(id_buffer[i]);
                    }
                }
                id_buffer.clear();
            }
            other => {
                return Err(anyhow!("Unexpected token {:?}", other).into());
            }
        }
    }
    if let Some(token) = token_it.next() {
        return Err(anyhow!("Unexpected token {:?}", token).into());
    }
    Ok(Graph {
        is_directed,
        nodes,
        adjacency,
    })
}

#[pymodule]
fn pydot_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse_file, m)?)?;
    Ok(())
}
