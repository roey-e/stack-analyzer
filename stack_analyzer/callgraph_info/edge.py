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
    ] = r"edge: \{ sourcename: \"(?P<sourcename>[\w\d_]+)\" targetname: \"(?P<targername>[\w\d_]+)\"( label: \"(?P<origin>\S*)\")? \}"
