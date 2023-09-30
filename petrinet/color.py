from literal import *


class Color:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name


class DotColor(Color):
    def __init__(self):
        super().__init__("dot")


class EnumerationColor(Color):
    values: list[EnumerationColorLiteral]

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.values = []

    def add(self, value: EnumerationColorLiteral) -> EnumerationColorLiteral:
        self.values.append(value)
        return value


class ProductColor(Color):
    types: list[EnumerationColor]

    def __init__(self, name: str, types: list[EnumerationColor] = None) -> None:
        super().__init__(name)
        self.types = types if types is not None else []
