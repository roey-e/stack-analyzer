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
