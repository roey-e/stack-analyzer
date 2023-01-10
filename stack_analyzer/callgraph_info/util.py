import dataclasses
import re
import typing


def is_type_optional(tp: typing.Type) -> bool:
    if typing.get_origin(tp) is typing.Union:
        args = typing.get_args(tp)
        return len(args) == 2 and type(None) in args


def get_optional_arg(tp: typing.Type[typing.Optional[typing.Type]]) -> typing.Type:
    if not is_type_optional(tp):
        raise ValueError("Not optional")

    first, second = typing.get_args(tp)
    return first if first is not type(None) else second


@dataclasses.dataclass
class ParsedDataclass:
    LINE_FORMAT: typing.ClassVar[str]

    def __post_init__(self):
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            true_type = field.type
            if is_type_optional(field.type):
                true_type = get_optional_arg(field.type)
            if value is not None and not isinstance(value, true_type):
                setattr(self, field.name, true_type(value))

    @classmethod
    def from_line(cls, line: str) -> "ParsedDataclass":
        pattern = re.compile(cls.LINE_FORMAT)
        match = pattern.match(line)
        if not match:
            raise Exception(f"Couldn't parse the line: '{line}'")

        return cls(**match.groupdict())
