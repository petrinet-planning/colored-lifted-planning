from __future__ import annotations

from .value import Value, EnumerationColorValue


class Variable(Value):

    def __init__(self, name: str, color: "Color") -> None:
        super().__init__(name, color)

    def generate_decl_pnml(self):
        return f'<variabledecl id="Var{self.strValue}" name="{self.strValue}"><usersort declaration="{self.color.name}"/></variabledecl>'

    def generate_pnml(self, weight: int):
        return f"""
            <subterm>
                <numberof>
                    <subterm><numberconstant value="{weight}"><positive/></numberconstant></subterm>
                    <subterm><variable refvariable="Var{self.strValue}"/></subterm>
                </numberof>
            </subterm>
        """


class EnumerationVariable(Variable, EnumerationColorValue):
    def __init__(self, name: str, color: "EnumerationColor") -> None:
        super().__init__(name, color)

    def generate_pnml_subterm(self):
        return f'<subterm><variable refvariable="Var{self.strValue}"/></subterm>'
    
    def __repr__(self):
        return f"{self.color.name}[{self.strValue}]"
