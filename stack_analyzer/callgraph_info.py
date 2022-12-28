import dataclasses
import re
from enum import Enum
from typing import ClassVar, List, Optional

from .stack_usage import StackUsageQualifier
from .util import get_optional_arg, is_type_optional


@dataclasses.dataclass
class CallgraphInfoNode:
    unique_name: str
    declared_name: str
    origin: str
    stack_usage: Optional[int] = None
    stack_usage_qualifier: Optional[StackUsageQualifier] = None

    LINE_FORMAT: ClassVar[
        str
    ] = r"node: \{ title: \"(?P<unique_name>[\w\d_]+)\" label: \"(?P<declared_name>[\w\d_]+)\\n(?P<origin>\S*)(\\n(?P<stack_usage>\d+) bytes \((?P<stack_usage_qualifier>[\w+,]+)\))?\".* \}"

    def __post_init__(self):
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            true_type = field.type
            if is_type_optional(field.type):
                true_type = get_optional_arg(field.type)
            if value is not None and not isinstance(value, true_type):
                setattr(self, field.name, true_type(value))

    @classmethod
    def parse_line(cls, line: str) -> "CallgraphInfoNode":
        pattern = re.compile(cls.LINE_FORMAT)
        match = pattern.match(line)
        if not match:
            raise Exception(f"Couldn't parse the line: '{line}'")
        print(match.groupdict())
        return cls(**match.groupdict())


@dataclasses.dataclass
class CallgraphInfoEdge:
    sourcename: str
    targername: str
    origin: str

    LINE_FORMAT: ClassVar[
        str
    ] = r"edge: \{ sourcename: \"(?P<sourcename>[\w\d_]+)\" targetname: \"(?P<targername>[\w\d_]+)\" label: \"(?P<origin>\S*)\" \}"

    @classmethod
    def parse_line(cls, line: str) -> "CallgraphInfoNode":
        pattern = re.compile(cls.LINE_FORMAT)
        match = pattern.match(line)
        if not match:
            raise Exception(f"Couldn't parse the line: '{line}'")

        return cls(**match.groupdict())


@dataclasses.dataclass
class CallgraphInfoGraph:
    title: str
    nodes: List[CallgraphInfoNode]
    edges: List[CallgraphInfoEdge]

    TITLE_FORMAT: ClassVar[str] = r"graph: \{ title: \"(?P<title>\S*)\""

    @classmethod
    def parse_text(cls, text: str) -> "CallgraphInfoGraph":
        pattern = re.compile(cls.TITLE_FORMAT)
        match = pattern.match(text)
        if not match:
            raise Exception(f"Couldn't parse the graph:\n'''{text}'''")

        nodes = []
        edges = []
        for line in text.splitlines():
            if line.strip().startswith("node"):
                nodes.append(CallgraphInfoNode.parse_line(line))
            elif line.strip().startswith("edge"):
                edges.append(CallgraphInfoEdge.parse_line(line))

        return cls(title=match.groupdict()["title"], nodes=nodes, edges=edges)
