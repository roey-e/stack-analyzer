import logging
import pathlib
import unittest

from stack_analyzer.callgraph_info.graph import CallgraphInfoGraph
from stack_analyzer.core import WeightedCallgraph


class SanityTest(unittest.TestCase):
    def test(self):
        for ci_path in pathlib.Path(__file__).parent.rglob("*.ci"):
            with self.subTest(ci_path.name):
                with open(ci_path) as ci_file:
                    ci_graph = CallgraphInfoGraph.from_text(ci_file.read())

                weighted_ci_graph = WeightedCallgraph.from_callgraph_info(ci_graph)

                stack_usage = weighted_ci_graph.max_stack_usage()
                callstack = weighted_ci_graph.max_stack_usage_callstack()

                logging.info(
                    "In %s, max stack usage of %u from the callstack: %s",
                    ci_path.name,
                    stack_usage,
                    callstack,
                )
