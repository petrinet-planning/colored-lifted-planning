from petrinet.color import Color
from petrinet.value import Value


class WeightedValues:
    values: dict[Value, int]
    color: Color

    def __init__(self, color: Color, values: dict[Value, int] = None):
        self.color = color
        self.values = values if values is not None else {}

        for v in self.values.keys():
            if v.color != self.color:
                raise Exception("Color Mismatch")

    def set(self, value: Value, weight):
        if value.color != self.color:
            raise Exception("Color Mismatch")

        self.values[value] = weight

    def items(self) -> list[tuple[Value, int]]:
        return self.values.items()
