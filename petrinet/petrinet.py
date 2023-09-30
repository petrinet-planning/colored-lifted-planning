from petrinet.place import Place
from petrinet.transition import Transition
from petrinet.arc import *
from petrinet.color import *
from petrinet.variable import *


class PetriNet:
    name: str
    colored: bool
    places: list[Place]
    transitions: list[Transition]
    arcs: list[Arc]
    colors: list[Color]
    variables: list[Variable]

    def __init__(self,
                 name: str,
                 places: list[Place] = None,
                 transitions: list[Transition] = None,
                 arcs: list[Arc] = None,
                 colors: list[Color] = None,
                 variables: list[Color] = None
                 ) -> None:
        super().__init__()

        self.name = name
        self.places = places if places is not None else []
        self.transitions = transitions if transitions is not None else []
        self.arcs = arcs if arcs is not None else []
        self.colors = colors if colors is not None else []
        self.variables = variables if variables is not None else []

    def add_place(self, place: Place) -> Place:
        self.places.append(place)
        return place

    def add_transition(self, transition: Transition) -> Transition:
        self.transitions.append(transition)
        return transition

    def add_arc(self, arc: Arc) -> Arc:
        if not self.places.__contains__(arc.place):
            raise "Attempted to add an arc containing a place not found in the petri net"

        if not self.transitions.__contains__(arc.transition):
            raise "Attempted to add an arc containing a transition not found in the petri net"

        self.arcs.append(arc)
        return arc

    def add_color(self, color: Color) -> Color:
        self.colors.append(color)
        return color

    def add_variable(self, variable: Variable) -> Variable:
        self.variables.append(variable)
        return variable
