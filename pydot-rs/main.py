import sys
from pure_python import parse_file as parse_file_py
from pydot_rs import parse_file as parse_file_rs

import timeit

if __name__ == "__main__":
    timeit_py = timeit.timeit(
        lambda: parse_file_py(sys.argv[1]), number=100, globals=globals()
    )
    print(f"pure-python: {timeit_py}")
    timeit_rs = timeit.timeit(
        lambda: parse_file_rs(sys.argv[1]), number=100, globals=globals()
    )
    print(f"pydot-rs: {timeit_rs}")
