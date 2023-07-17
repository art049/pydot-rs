use regex::Regex;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Token {
    Graph,
    Digraph,
    LeftBracket,
    RightBracket,
    Semicolon,
    Edge,
    Identifier(String),
}

pub fn word_to_token(word: &str) -> Token {
    match word {
        "graph" => Token::Graph,
        "digraph" => Token::Digraph,
        "{" => Token::LeftBracket,
        "}" => Token::RightBracket,
        ";" => Token::Semicolon,
        "--" => Token::Edge,
        _ => Token::Identifier(word.to_string()),
    }
}

pub fn split_words(text: &str) -> Vec<&str> {
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
}
