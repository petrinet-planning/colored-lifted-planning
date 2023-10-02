from __future__ import annotations
from typing import Union

from petrinet.color import Color, ProductColor


class Value:
    color: "Color"
    strValue: str

    def __init__(self, strValue: str, color: "Color"):
        self.strValue = strValue
        self.color = color

    def generate_pnml(self, weight: int):
        raise Exception("Not Implemented")


class ProductColorValue(Value):
    values: list[Union["EnumerationColorLiteral", "Variable"]]

    def __init__(self, color: "Color", values: list[Union["EnumerationColorLiteral", "Variable"]]) -> None:
        if not isinstance(color, ProductColor):
            raise Exception("Product must be of product type")

        name = f'({[v.strValue for v in values]})'

        super().__init__(name, color)
        self.values = values

    def generate_pnml(self, weight: int):
        newline = "\n"

        return f'''\
        <subterm>
            <numberof>
                <subterm>
                    <numberconstant value="{weight}"><positive/></numberconstant>
                </subterm>
                <subterm>
                    <tuple>
                        {newline.join([f'<subterm><variable refvariable="Var{v.strValue}"/></subterm>' for v in self.values])}
                    </tuple>
                </subterm>
            </numberof>
        </subterm>
        '''