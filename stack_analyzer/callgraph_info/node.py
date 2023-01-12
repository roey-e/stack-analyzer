from dataclasses import dataclass
from typing import ClassVar, Optional

from .util import ParsedDataclass


@dataclass
class CallgraphInfoNode(ParsedDataclass):
    name: str
    declared_name: str
    origin: str
    stack_usage: Optional[int] = None
    stack_usage_qualifier: Optional[str] = None

    LINE_FORMAT: ClassVar[
        str
    ] = r"node: \{ title: \"(?P<name>\S+)\" label: \"(?P<declared_name>[\w\d_]+)\\n(?P<origin>\S*)(\\n(?P<stack_usage>\d+) bytes \((?P<stack_usage_qualifier>[\w,]+)\))?\".* \}"
