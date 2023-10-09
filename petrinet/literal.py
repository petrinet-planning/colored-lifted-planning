from __future__ import annotations

from .value import Value


class Literal(Value):
    def __init__(self, name: str, color: "Color") -> None:
        super().__init__(name, color)

    def generate_pnml(self, weight: int):
        return f"""
            <subterm>
                <numberof>
                    <subterm><numberconstant value="{weight}"><positive/></numberconstant></subterm>
                    <subterm><useroperator declaration="{self.strValue}"/></subterm>
                </numberof>
            </subterm>
        """


class DotColorLiteral(Literal):
    def __init__(self, color: "DotColor") -> None:
        super().__init__("dot", color)


class EnumerationColorLiteral(Literal):
    def __init__(self, color: "EnumerationColor", value: str) -> None:
        super().__init__(value, color)


class ProductColorLiteral(Literal):
    values: list["EnumerationColorLiteral"]

    def __init__(self, color: "Color", values: list["EnumerationColorLiteral"]) -> None:
        super().__init__(f'({", ".join([val.strValue for val in values])})', color)
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
                        {newline.join([f'<subterm><useroperator declaration="{v.strValue}"/></subterm>' for v in self.values])}
                    </tuple>
                </subterm>
            </numberof>
        </subterm>
        '''
