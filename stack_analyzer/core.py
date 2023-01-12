from itertools import chain
from typing import List, Tuple

import networkx as nx

from .callgraph_info.graph import CallgraphInfoGraph

DUMMY_SIGN = "!"


class WeightedCallgraph(nx.DiGraph):
    @classmethod
    def from_callgraph_info(cls, graph: CallgraphInfoGraph) -> "WeightedCallgraph":
        weighted_graph = cls()

        dummy_edges: List[Tuple[str, str]] = []
        for node in graph.nodes:
            dummy_node = cls.get_dummy_node(node)

            weighted_graph.add_nodes_from([node, dummy_node])

            dummy_edges.append((dummy_node, node))

        for src, dst in chain(graph.edges, dummy_edges):
            stack_usage = graph.nodes[dst]["stack_usage"] or 0
            weighted_graph.add_edge(src, dst, weight=stack_usage)

        weighted_graph.break_cycles()

        return weighted_graph

    @staticmethod
    def is_dummy_node(node: str) -> bool:
        return node.startswith(DUMMY_SIGN)

    @classmethod
    def get_dummy_node(cls, node: str) -> str:
        return f"{DUMMY_SIGN}{node}" if not cls.is_dummy_node(node) else node

    def break_cycles(self):
        for cycle in nx.simple_cycles(self):
            self.remove_edge(cycle[-1], cycle[0])

    def subgraph_from(self, source: str) -> "WeightedCallgraph":
        source = self.get_dummy_node(source)

        nodes = [source]
        nodes.extend(nx.descendants(self, source))

        return self.subgraph(nodes)
