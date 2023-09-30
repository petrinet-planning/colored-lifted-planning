from typing import Union

from petrinet.place import Place
from petrinet.transition import Transition
from value import Value
from color import EnumerationColorLiteral

class Arc:
    name: str
    place: Place
    transition: Transition
    value: Value
    weight: int

    def __init__(self, place: Place, transition: Transition, value: Value, weight: int = None) -> None:
        if place.color != value.color:
            raise "Incompatible types, " + str(place.color) + "and" + str(place.color)

        self.place = place
        self.transition = transition
        self.value = value
        self.weight = weight if weight is not None else 1


class ArcPlaceToTransition(Arc):
    def __init__(self, place: Place, transition: Transition, value: Value) -> None:
        super().__init__(place, transition, value)


class ArcTransitionToPlace(Arc):
    def __init__(self, transition: Transition, place: Place, value: Value) -> None:
        super().__init__(place, transition, value)

