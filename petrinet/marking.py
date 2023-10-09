from .literal import Literal
from .place import Place
from .weighted_values import WeightedValues


class Marking:
    values: dict[Place, WeightedValues]

    def __init__(self) -> None:
        self.values = dict()

    def set(self, place: Place, literal: Literal, weight: int = 1) -> None:
        # todo: Clean up literals with a weight of 0

        self.values[place] = self.values.get(place, WeightedValues(place.color))
        self.values[place].set(literal, weight)

    def get(self, place: Place) -> WeightedValues:
        return self.values.get(place, {})

    def generate_pnml(self, place: Place) -> str:
        newline = "\n"
        literal_weight_pairs = self.get(place).items()

        if len(literal_weight_pairs) == 0:
            return ""

        return f'''\
                <hlinitialMarking>
                    <text>({" + ".join([f"{weight}'{literal.strValue}" for (literal, weight) in literal_weight_pairs])})</text>
                    <structure>
                        <add>\
                        {newline.join([literal.generate_pnml(weight) for (literal, weight) in literal_weight_pairs])}
                        </add>
                    </structure>
                </hlinitialMarking>
                '''
