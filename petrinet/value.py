from typing import Union

from color import Color, ProductColor
from petrinet.literal import EnumerationColorLiteral
from petrinet.variable import Variable


class Value:
    color: Color

    def __init__(self, color: Color):
        self.color = color


class ProductColorValue(Value):
    values: list[Union[EnumerationColorLiteral, Variable]]

    def __init__(self, color: Color, values: list[Union[EnumerationColorLiteral, Variable]]) -> None:
        if color is not Color:
            raise "Product must be of product type"

        super().__init__(color)
        self.values = values
