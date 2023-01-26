import logging
import pathlib
import unittest
from typing import ClassVar

import networkx as nx

from stack_analyzer.callgraph_info.graph import CallgraphInfoGraph
from stack_analyzer.core import WeightedCallgraph


class HtopTest(unittest.TestCase):

    SOURCE_DIR: ClassVar[pathlib.Path] = pathlib.Path(__file__).parent / "htop"

    def test_sanity(self):
        for ci_path in self.SOURCE_DIR.rglob("*.ci"):
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

    def test_source(self):
        CI_PATH = next(self.SOURCE_DIR.rglob("Settings.ci"))
        SOURCE = "Settings.c:ScreenSettings_readFields"
        EXPECTED_NODES = [SOURCE, "Settings.c:toFieldIndex"]
        EXPECTED_STACK_USAGE = 96 + 96

        with open(CI_PATH) as ci_file:
            ci_graph = CallgraphInfoGraph.from_text(ci_file.read())

        weighted_ci_graph = WeightedCallgraph.from_callgraph_info(ci_graph)

        stack_usage = weighted_ci_graph.max_stack_usage(SOURCE)
        callstack = weighted_ci_graph.max_stack_usage_callstack(SOURCE)

        logging.info(
            "In %s, max stack usage of %u from the callstack: %s",
            CI_PATH.name,
            stack_usage,
            callstack,
        )

        for node in EXPECTED_NODES:
            self.assertIn(node, (node for node, stack_usage in callstack))
        self.assertEqual(EXPECTED_STACK_USAGE, stack_usage)

    def test_joint(self):
        ci_graphs = []
        for ci_path in self.SOURCE_DIR.rglob("*.ci"):
            with open(ci_path) as ci_file:
                ci_graphs.append(CallgraphInfoGraph.from_text(ci_file.read()))

        joint_ci_graph = nx.compose_all(ci_graphs)
        weighted_ci_graph = WeightedCallgraph.from_callgraph_info(joint_ci_graph)

        stack_usage = weighted_ci_graph.max_stack_usage()
        callstack = weighted_ci_graph.max_stack_usage_callstack()

        logging.info(
            "Max stack usage of %u from the callstack: %s",
            stack_usage,
            callstack,
        )


class FactorialTest(unittest.TestCase):

    SOURCE_DIR: ClassVar[pathlib.Path] = pathlib.Path(__file__).parent / "factorial"

    # Checking the cycles are cut as expected.
    def test(self):
        CI_PATH = next(self.SOURCE_DIR.rglob("*.ci"))

        with open(CI_PATH) as ci_file:
            ci_graph = CallgraphInfoGraph.from_text(ci_file.read())

        # Making sure testing recursion.
        self.assertFalse(nx.is_directed_acyclic_graph(ci_graph))

        weighted_ci_graph = WeightedCallgraph.from_callgraph_info(ci_graph)

        stack_usage = weighted_ci_graph.max_stack_usage()
        callstack = weighted_ci_graph.max_stack_usage_callstack()

        logging.info(
            "In %s, max stack usage of %u from the callstack: %s",
            CI_PATH.name,
            stack_usage,
            callstack,
        )
