from __future__ import annotations
from .color import Color, ProductColor


class Value:
    color: "Color"
    strValue: str
    displayName: str

    def __init__(self, strValue: str, color: "Color"):
        self.strValue = strValue
        self.display_name = strValue
        self.color = color

    def generate_pnml(self, weight: int):
        raise Exception("Not Implemented")

    def __repr__(self):
        return f"{self.color.name}[{self.strValue}]"

class EnumerationColorValue(Value):
    def generate_pnml_subterm(self):
        pass

class ProductColorValue(Value):
    values: list["EnumerationColorValue"]

    def __init__(self, color: "Color", values: list[EnumerationColorValue]) -> None:
        if not isinstance(color, ProductColor):
            raise Exception("Product must be of product type")

        name = f'({[v.strValue for v in values]})'

        super().__init__(name, color)
        self.values = values

    def generate_pnml(self, weight: int):
        newline = "\n"

        # subterms = [
        #     f'<subterm><variable refvariable="Var{val.strValue}"/></subterm>' if type(val) is Variable else
        #     f'<subterm><useroperator declaration="{val.strValue}" /></subterm>'
        #     for val in self.values]


        return f'''\
        <subterm>
            <numberof>
                <subterm>
                    <numberconstant value="{weight}"><positive/></numberconstant>
                </subterm>
                <subterm>
                    <tuple>
                        {newline.join([val.generate_pnml_subterm() for val in self.values])}
                    </tuple>
                </subterm>
            </numberof>
        </subterm>
        '''