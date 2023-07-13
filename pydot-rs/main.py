import rustimport.import_hook  # noqa: F401 # type: ignore
import sys
import dot_python
import dot_rust


import timeit

if __name__ == "__main__":
    timeit_py = timeit.timeit(
        lambda: dot_python.parse_file(sys.argv[1]), number=100, globals=globals()
    )
    print(f"pure-python: {timeit_py}")
    timeit_rs = timeit.timeit(
        lambda: dot_rust.parse_file(sys.argv[1]), number=100, globals=globals()
    )
    print(f"pydot-rs: {timeit_rs}")
