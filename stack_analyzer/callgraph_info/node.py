from dataclasses import dataclass
from typing import ClassVar, Optional

from .util import ParsedDataclass


@dataclass
class CallgraphInfoNode(ParsedDataclass):
    name: str
    declared_name: Optional[str] = None
    origin: Optional[str] = None
    stack_usage: Optional[int] = None
    stack_usage_qualifier: Optional[str] = None

    LINE_FORMAT: ClassVar[
        str
    ] = r'node: \{ title: "(?P<name>\S+)" label: "((?P<declared_name>\S+)\\n(?P<origin>\S*)|Indirect Call Placeholder)(\\n(?P<stack_usage>\d+) bytes \((?P<stack_usage_qualifier>[\w,]+)\))?".* \}'
