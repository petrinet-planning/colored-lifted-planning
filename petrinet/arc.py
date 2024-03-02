from __future__ import annotations
from typing import Union

from .value import Value
from .weighted_values import WeightedValues


class Arc:
    name: str
    place: "Place"
    transition: "Transition"
    values: WeightedValues

    def __init__(self, name: str, place: "Place", transition: "Transition", values: Union[dict[Value, int], WeightedValues] = None) -> None:
        self.name = name
        self.place = place
        self.transition = transition

        if isinstance(values, WeightedValues):
            if values.color != self.place.color:
                raise Exception("Value color must match place color")
            self.values = values
        else:
            self.values = WeightedValues(place.color)
            if values is not None:
                self.values.absorb(values)

    def set_weight(self, value: "Value", weight: int):
        self.values.set(value, weight)

    def get_source(self) -> Union["Place", "Transition"]:
        raise Exception("Not implemented on base class")

    def get_destination(self) -> Union["Place", "Transition"]:
        raise Exception("Not implemented on base class")

    def absorb(self, other: Arc):
        if self.get_source() != other.get_source():
            raise Exception("Arc sources must match for merge")
        if self.get_destination() != other.get_destination():
            raise Exception("Arc destinations must match for merge")

        self.values.absorb(other.values)

    def generate_pnml(self):
        raise Exception("Not Implemented")


class ArcPlaceToTransition(Arc):
    def __init__(self, place: "Place", transition: "Transition", values: Union[dict[Value, int], WeightedValues] = None) -> None:
        super().__init__(f'{place.name}_to_{transition.name}', place, transition, values)

    def get_source(self) -> Union["Place", "Transition"]:
        return self.place

    def get_destination(self) -> Union["Place", "Transition"]:
        return self.transition

    def generate_pnml(self):
        newline = "\n"

        return f'''\
            <arc id="{self.name}" source="{self.place.name}" target="{self.transition.name}" type="normal">
                <hlinscription>
                    <text>({" + ".join([f"{weight}'{val.display_name}" for val,weight in self.values.items()])})</text>
                    <structure>
                        <add>
                            {newline.join([val.generate_pnml(weight) for (val, weight) in self.values.items()])}
                        </add>
                    </structure>
                </hlinscription>
            </arc>
        '''


class ArcTransitionToPlace(Arc):
    def __init__(self, transition: "Transition", place: "Place", values: Union[dict[Value, int], WeightedValues] = None) -> None:
        super().__init__(f'{transition.name}_to_{place.name}', place, transition, values)

    def get_source(self) -> Union["Place", "Transition"]:
        return self.transition

    def get_destination(self) -> Union["Place", "Transition"]:
        return self.place

    def generate_pnml(self):
        newline = "\n"

        return f'''\
            <arc id="{self.name}" source="{self.transition.name}" target="{self.place.name}" type="normal">
                <hlinscription>
                    <text>({" + ".join([f"{weight}'{val.display_name}" for val,weight in self.values.items()])})</text>
                    <structure>
                        <add>
                            {newline.join([val.generate_pnml(weight) for (val, weight) in self.values.items()])}
                        </add>
                    </structure>
                </hlinscription>
            </arc>
        '''
