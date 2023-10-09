from typing import Union

from petrinet.marking import Marking
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
    arc_dict: dict[tuple[Union[Place, Transition], Union[Place, Transition]], Arc]
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
        self.arcs = []
        self.arc_dict = dict()
        if arcs is not None:
            for arc in arcs:
                self.add_arc(arc)
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

        src = arc.get_source()
        dest = arc.get_destination()

        existing_arc = self.arc_dict.get((src, dest), None)

        if existing_arc is not None:
            existing_arc.absorb(arc)
            return existing_arc

        else:
            self.arcs.append(arc)
            self.arc_dict[src, dest] = arc
            return arc

    def add_color(self, color: Color) -> Color:
        self.colors.append(color)
        return color

    def add_variable(self, variable: Variable) -> Variable:
        self.variables.append(variable)
        return variable

    def generate_pnml(self, marking: Marking) -> str:
        newline = "\n"

        color_decls = newline.join([color.generate_pnml() for color in self.colors])

        var_decls = newline.join([var.generate_decl_pnml() for var in self.variables])

        places = newline.join([place.generate_pnml(marking, position=(100+150*i, 100)) for i, place in enumerate(self.places)])

        transitions = newline.join([transition.generate_pnml(position=(175+150*i, 300)) for i, transition in enumerate(self.transitions)])

        arcs = newline.join([arc.generate_pnml() for arc in self.arcs])

        return f'''\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<pnml xmlns="http://www.pnml.org/version-2009/grammar/pnml">
    <net id="ComposedModel" type="http://www.pnml.org/version-2009/grammar/ptnet">
        <name><text>ComposedModel</text></name>
        <declaration>
            <structure>
                <declarations>
                {color_decls}
                {var_decls}
                </declarations>
            </structure>
        </declaration>
        <page id="page0">
            {places}
            {transitions}
            {arcs}
        </page>
    </net>
</pnml>
'''
