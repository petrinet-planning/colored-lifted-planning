from value import Value
from color import Color


class Variable(Value):
    name: str

    def __init__(self, name: str, color: Color) -> None:
        super().__init__(color)
        self.name = name
