from __future__ import annotations


class Color:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def generate_pnml(self) -> str:
        raise "Not Implemented"

    def __repr__(self):
        return self.name
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Color):
            return False
        
        return self.name == __value.name


class DotColor(Color):
    def __init__(self):
        super().__init__("dot")

    def generate_pnml(self) -> str:
        return f'<namedsort id="{self.name}" name="{self.name}"> <dot/> </namedsort>'


class EnumerationColor(Color):
    values: list["EnumerationColorLiteral"]

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.values = []

    def add(self, value: "EnumerationColorLiteral") -> "EnumerationColorLiteral":
        self.values.append(value)
        return value

    def generate_pnml(self) -> str:
        newline = "\n"
        return f'''\
            <namedsort id="{self.name}" name="{self.name}">
                <cyclicenumeration>
                    { newline.join([f'<feconstant id="{v.strValue}" name="{self.name}"/>' for v in self.values]) }
                </cyclicenumeration>
            </namedsort>'''
    
    def __eq__(self, __value: object) -> bool:
        if not Color.__eq__(self, __value):
            return False
        
        return self.values == __value.values


class ProductColor(Color):
    types: list["EnumerationColor"]

    def __init__(self, name: str, types: list["EnumerationColor"] = None) -> None:
        super().__init__(name)
        self.types = types if types is not None else []

    def generate_pnml(self) -> str:
        newline = "\n"
        return f'''\
            <namedsort id="{self.name}" name="{self.name}"><productsort>
                {newline.join([f'<usersort declaration="{t.name}"/>' for t in self.types])}
            </productsort></namedsort>'''

    def __eq__(self, __value: object) -> bool:
        if not Color.__eq__(self, __value):
            return False
        
        return self.types == __value.types
    