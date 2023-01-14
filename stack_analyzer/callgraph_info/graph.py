import re
from typing import ClassVar

import networkx as nx

from .edge import CallgraphInfoEdge
from .node import CallgraphInfoNode


class CallgraphInfoGraph(nx.DiGraph):

    TITLE_FORMAT: ClassVar[str] = r"graph: \{ title: \"(?P<title>\S*)\""

    def add_node(self, node: CallgraphInfoNode) -> None:
        super().add_node(node.name, **node.as_clean_dict())

    def add_edge(self, edge: CallgraphInfoEdge) -> None:
        super().add_edge(edge.sourcename, edge.targername, **edge.as_clean_dict())

    @classmethod
    def from_text(cls, text: str) -> "CallgraphInfoGraph":
        pattern = re.compile(cls.TITLE_FORMAT)
        match = pattern.match(text)
        if not match:
            raise Exception(f"Couldn't parse the graph:\n'''{text}'''")

        graph = cls(**match.groupdict())

        for line in text.splitlines():
            if line.strip().startswith("node"):
                graph.add_node(CallgraphInfoNode.from_line(line))
            elif line.strip().startswith("edge"):
                graph.add_edge(CallgraphInfoEdge.from_line(line))

        return graph

    def __str__(self) -> str:
        return f"{self.graph['title']}:\nNodes: {self.nodes(data=True)}\nEdges: {self.edges(data=True)}"
