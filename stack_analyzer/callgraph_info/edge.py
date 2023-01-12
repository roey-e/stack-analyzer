from dataclasses import dataclass
from typing import ClassVar, Optional

from .util import ParsedDataclass


@dataclass
class CallgraphInfoEdge(ParsedDataclass):
    sourcename: str
    targername: str
    origin: Optional[str] = None

    LINE_FORMAT: ClassVar[
        str
    ] = r"edge: \{ sourcename: \"(?P<sourcename>\S+)\" targetname: \"(?P<targername>\S+)\"( label: \"(?P<origin>\S*)\")? \}"
