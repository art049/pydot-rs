// rustimport:pyo3
use pyo3::prelude::*;

use std::collections::HashMap;

mod parser;
use parser::Parser;
mod tokenizer;
use tokenizer::{split_words, word_to_token};

#[pyclass]
#[derive(Debug)]
pub struct Graph {
    pub graph_name: String,
    pub nodes: Vec<String>,
    pub adjacency: HashMap<usize, Vec<usize>>,
}

#[pyfunction]
pub fn parse_file(filepath: String) -> PyResult<Graph> {
    let text = std::fs::read_to_string(filepath)?;
    let words_it = split_words(&text).into_iter();
    let mut token_it = words_it.map(word_to_token);
    let mut parser = Parser::new();
    let graph = parser.parse(&mut token_it);
    Ok(graph)
}
