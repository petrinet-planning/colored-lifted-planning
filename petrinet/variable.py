from __future__ import annotations

from .value import Value, EnumerationColorValue


class Variable(Value):

    def __init__(self, id: str, display_name: str, color: "Color") -> None:
        super().__init__(id, color)
        self.display_name = display_name

    def generate_decl_pnml(self):
        return f'<variabledecl id="{self.strValue}" name="{self.display_name}"><usersort declaration="{self.color.name}"/></variabledecl>'

    def generate_pnml(self, weight: int):
        return f"""
            <subterm>
                <numberof>
                    <subterm><numberconstant value="{weight}"><positive/></numberconstant></subterm>
                    <subterm><variable refvariable="{self.strValue}"/></subterm>
                </numberof>
            </subterm>
        """


class EnumerationVariable(Variable, EnumerationColorValue):
    def __init__(self, id: str, display_name: str, color: "EnumerationColor") -> None:
        super().__init__(id, display_name, color)

    def generate_pnml_subterm(self):
        return f'<subterm><variable refvariable="{self.strValue}"/></subterm>'
    
    def __repr__(self):
        return f"{self.color.name}[{self.strValue}]"
