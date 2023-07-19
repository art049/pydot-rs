import rustimport.import_hook  # noqa: F401 # type: ignore

# Make a release build of the Rust binaries
rustimport.settings.compile_release_binaries = True

from .dot_python import parse_file as parse_file_py
from .dot_python import Graph
from .dot_rust import parse_file as parse_file_rs

parse_file = parse_file_rs

__all__ = ["parse_file", "parse_file_py", "parse_file_rs", "Graph"]
