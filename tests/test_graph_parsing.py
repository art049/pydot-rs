import pytest
from pydot_rs import parse_file_rs, parse_file_py, Graph


# Parametrized fixture to test both implementations
@pytest.fixture(
    params=[
        pytest.param(parse_file_rs, id="rust"),
        pytest.param(parse_file_py, id="python"),
    ]
)
def parse_file_impl(request):
    return request.param


def test_parsing_small(parse_file_impl, benchmark):
    graph: Graph = benchmark(parse_file_impl, "samples/undir.dot")
    assert graph.graph_name == "MyCoolUndirectedGraph"
    assert len(graph.nodes) == 4
    assert set(graph.nodes) == {"a", "b", "c", "d"}


def test_parsing_big(parse_file_impl, benchmark):
    graph: Graph = benchmark(parse_file_impl, "samples/graph.dot")
    assert graph.graph_name == "BigGraph"
    assert len(graph.nodes) == 1000
