from pydot_rs import parse_file, Graph


def test_parsing_default_small(benchmark):
    graph: Graph = benchmark(parse_file, "samples/undir.dot")
    assert graph.graph_name == "MyCoolUndirectedGraph"
    assert len(graph.nodes) == 4
    assert set(graph.nodes) == {"a", "b", "c", "d"}


def test_parsing_default_big(benchmark):
    graph: Graph = benchmark(parse_file, "samples/graph.dot")
    assert graph.graph_name == "BigGraph"
    assert len(graph.nodes) == 1000
