from petrinet.literal import Literal
from petrinet.place import Place


class Marking:
    values: dict[Place, dict[Literal, int]]

    def __init__(self) -> None:
        self.values = {}

    def set(self, place: Place, literal: Literal, weight: int = 1) -> None:
        # todo: Clean up literals with a weight of 0

        if self.values[place] is None:
            self.values[place] = {}

        self.values[place][literal] = weight
