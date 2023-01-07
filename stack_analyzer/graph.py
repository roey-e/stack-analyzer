import re
from typing import ClassVar

import networkx as nx

from .callgraph_info import CallgraphInfoEdge, CallgraphInfoNode


class CallgraphInfoGraph:

    TITLE_FORMAT: ClassVar[str] = r"graph: \{ title: \"(?P<title>\S*)\""

    def __init__(self, title: str) -> None:
        self.graph = nx.DiGraph(title=title)

    def add_node(self, node: CallgraphInfoNode) -> None:
        self.graph.add_node(node.unique_name, data=node)

    def add_edge(self, edge: CallgraphInfoEdge) -> None:
        self.graph.add_edge(edge.sourcename, edge.targername, data=edge)

    @classmethod
    def from_text(cls, text: str) -> "CallgraphInfoGraph":
        pattern = re.compile(cls.TITLE_FORMAT)
        match = pattern.match(text)
        if not match:
            raise Exception(f"Couldn't parse the graph:\n'''{text}'''")

        graph = cls(match.groupdict()["title"])

        for line in text.splitlines():
            if line.strip().startswith("node"):
                graph.add_node(CallgraphInfoNode.parse_line(line))
            elif line.strip().startswith("edge"):
                graph.add_edge(CallgraphInfoEdge.parse_line(line))

        return graph
