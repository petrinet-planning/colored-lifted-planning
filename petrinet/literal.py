from value import Value, ProductColorValue
from color import Color, DotColor, EnumerationColor, ProductColor


class Literal(Value):
    def __init__(self, color: Color) -> None:
        super().__init__(color)


class DotColorLiteral(Literal):
    def __init__(self, color: DotColor) -> None:
        super().__init__(color)


class EnumerationColorLiteral(Literal):
    value: str

    def __init__(self, color: EnumerationColor, value: str) -> None:
        super().__init__(color)
        self.value = value


class ProductColorLiteral(Literal):
    values: list[EnumerationColorLiteral]

    def __init__(self, color: Color, values: list[EnumerationColorLiteral]) -> None:
        super().__init__(color)
        self.values = values
