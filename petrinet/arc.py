from __future__ import annotations

from petrinet.value import Value
from petrinet.weighted_values import WeightedValues


class Arc:
    name: str
    place: "Place"
    transition: "Transition"
    values: WeightedValues

    def __init__(self, name: str, place: "Place", transition: "Transition", values: dict[Value, int] = None) -> None:
        self.name = name
        self.place = place
        self.transition = transition
        self.values = WeightedValues(place.color, values) if values is not None else WeightedValues(place.color)

    def set_weight(self, value: "Value", weight: int):
        self.values.set(value, weight)

    def generate_pnml(self):
        raise Exception("Not Implemented")


class ArcPlaceToTransition(Arc):
    def __init__(self, place: "Place", transition: "Transition", values: dict[Value, int]) -> None:
        super().__init__(f'{place.name}_to_{transition.name}', place, transition, values)

    def generate_pnml(self):
        newline = "\n"

        return f'''\
            <arc id="{self.name}" source="{self.place.name}" target="{self.transition.name}" type="normal">
                <hlinscription>
                    <text>({" + ".join([f"{weight}'{val.strValue}" for val,weight in self.values.items()])})</text>
                    <structure>
                        <add>
                            {newline.join([val.generate_pnml(weight) for (val, weight) in self.values.items()])}
                        </add>
                    </structure>
                </hlinscription>
            </arc>
        '''


class ArcTransitionToPlace(Arc):
    def __init__(self, transition: "Transition", place: "Place", values: dict[Value, int]) -> None:
        super().__init__(f'{transition.name}_to_{place.name}', place, transition, values)

    def generate_pnml(self):
        newline = "\n"

        return f'''\
            <arc id="{self.name}" source="{self.transition.name}" target="{self.place.name}" type="normal">
                <hlinscription>
                    <text>({" + ".join([f"{weight}'{val.strValue}" for val,weight in self.values.items()])})</text>
                    <structure>
                        <add>
                            {newline.join([val.generate_pnml(weight) for (val, weight) in self.values.items()])}
                        </add>
                    </structure>
                </hlinscription>
            </arc>
        '''
