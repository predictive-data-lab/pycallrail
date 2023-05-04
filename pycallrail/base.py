import typing

class CallRailBase(object):
    def __init__(self) -> None:
        self.id: typing.Union[str, None, int] = None

    def __hash__(self) -> int:
        class_name = type(self).__name__
        return hash((class_name, self.id))