from pydot_rs import parse_file, Graph


def test_parsing_default_big(benchmark):
    graph: Graph = benchmark(parse_file, "samples/graph.dot")
    assert graph.graph_name == "BigGraph"
    assert len(graph.nodes) == 1000
