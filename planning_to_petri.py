import re

from petrinet import petrinet
from petrinet.arc import ArcPlaceToTransition, ArcTransitionToPlace
from petrinet.color import *
from petrinet.literal import EnumerationColorLiteral, DotColorLiteral, ProductColorLiteral
from petrinet.marking import Marking
from petrinet.petrinet import PetriNet
from petrinet.place import Place
from petrinet.value import ProductColorValue
from petrinet.variable import *
from petrinet.transition import *
from petrinet.weighted_values import WeightedValues
from unified_planning.model import Problem, Action, OperatorKind


def translate(name: str, problem: Problem) -> tuple[PetriNet, Marking]:
    pn = petrinet.PetriNet("Blocksworld_p01")

    # Objects
    dotColor = DotColor()
    dotLiteral = DotColorLiteral(dotColor)
    objectsColor = EnumerationColor("objects")
    objects = {}
    for obj in problem.all_objects:
        objects[obj.name] = objectsColor.add(EnumerationColorLiteral(objectsColor, obj.name))

    # Predicates and Actions

    # ParamColors
    param_colors: dict[int, Color] = dict()
    param_colors[0] = pn.add_color(dotColor)
    param_colors[1] = pn.add_color(objectsColor)
    param_colors[2] = pn.add_color(ProductColor("params_2", [objectsColor, objectsColor]))

    # Variables
    variables: dict[str, Variable] = dict()
    for action in problem.actions:
        for parameter in action.parameters:
            if not variables.get(parameter.name):
                variables[parameter.name] = pn.add_variable(Variable(parameter.name, objectsColor))

    # Predicates / Places
    places: dict[str, Place] = dict()
    for pred in problem.fluents:
        places[pred.name] = pn.add_place(Place("pred_" + pred.name, param_colors[pred.arity]))

    # Actions / Transitions
    transitions: dict[str, Transition] = dict()

    def action_atom_types(action: Action) -> list[tuple[str, str]]:
        print(action)
        in_pre = 0b100
        in_del = 0b010
        in_add = 0b001
        occurrences: dict[str, int] = {}

        if action.preconditions[0].node_type is OperatorKind.FLUENT_EXP:
            pred_str = str(action.preconditions[0])
            occurrences[pred_str] = occurrences.get(pred_str, 0) | in_pre
        elif action.preconditions[0].node_type is OperatorKind.AND:  # Only one precondition
            for pred in action.preconditions[0].args:
                occurrences[str(pred)] = occurrences.get(str(pred), 0) | in_pre
        else:
            raise "Unhandled pred type"

        for eff in action.effects:
            if str(eff.value) == "true":
                occurrences[str(eff.fluent)] = occurrences.get(str(eff.fluent), 0) | in_add
            else:
                occurrences[str(eff.fluent)] = occurrences.get(str(eff.fluent), 0) | in_del

        occurrence_types: [int, str] = dict()
        occurrence_types[in_pre | in_del | in_add] = "requires"
        occurrence_types[in_pre | in_del |      0] = "deletes"
        occurrence_types[in_pre |      0 | in_add] = "requires"
        occurrence_types[in_pre |      0 |      0] = "requires"
        occurrence_types[     0 | in_del | in_add] = "adds"
        occurrence_types[     0 | in_del |      0] = "UNSUPPORTED"
        occurrence_types[     0 |      0 | in_add] = "adds"
        occurrence_types[     0 |      0 |      0] = "not in"

        # Check validity
        for pred, occ in occurrences.items():
            if occurrence_types[occ] == "UNSUPPORTED":
                raise Exception("Unsupported predicate type - del without pre")
            if occurrence_types[occ] == "not in":
                raise Exception("Should not happen - pred exists, but doesn't")

        return [(pred, occurrence_types[occ]) for pred, occ in occurrences.items()]

    pred_to_place_regex = re.compile("^[\\w_-]+")  # Finds first bit, until first parenthesis
    pred_parameter_regex = re.compile("([\\w_-]+)(?:, |\\))")  # Finds every variable, as any word ending with comma or closing parenthesis
    for action in problem.actions:
        transition = pn.add_transition(Transition(action.name))
        transitions[action.name] = transition

        for pred, type in action_atom_types(action):
            place = places[pred_to_place_regex.search(pred).group()]
            action_parameter_names = pred_parameter_regex.findall(pred)

            arc_weights: dict[Value, int] = dict()
            if len(action_parameter_names) > 1:
                action_parameters = [variables[param_name] for param_name in action_parameter_names]
                value = ProductColorValue(param_colors[len(action_parameter_names)], action_parameters)
                arc_weights[value] = 1

            elif len(action_parameter_names) == 1:
                arc_weights[variables[action_parameter_names[0]]] = 1

            else:
                arc_weights[dotLiteral] = 1

            if type == "requires":
                pn.add_arc(ArcPlaceToTransition(place, transition, arc_weights))
                pn.add_arc(ArcTransitionToPlace(transition, place, arc_weights))
            elif type == "deletes":
                pn.add_arc(ArcPlaceToTransition(place, transition, arc_weights))
            elif type == "adds":
                pn.add_arc(ArcTransitionToPlace(transition, place, arc_weights))
            else:
                raise "Unhandled relationship type: " + type

    # Markings
    # Initial
    initialMarking = Marking()
    initialMarking.set(places["clear"], objects["b1"], 1)
    initialMarking.set(places["clear"], objects["b2"], 1)
    initialMarking.set(places["clear"], objects["b5"], 1)
    initialMarking.set(places["on-table"], objects["b3"], 1)
    initialMarking.set(places["on-table"], objects["b4"], 1)
    initialMarking.set(places["on-table"], objects["b5"], 1)
    initialMarking.set(places["arm-empty"], dotLiteral, 1)
    initialMarking.set(places["on"], ProductColorLiteral(param_colors[2], [objects["b1"], objects["b4"]]), 1)
    initialMarking.set(places["on"], ProductColorLiteral(param_colors[2], [objects["b2"], objects["b3"]]), 1)

    # Goal
    goalMarking = Marking()
    goalMarking.set(places["on"], ProductColorLiteral(param_colors[2], [objects["b1"], objects["b4"]]), 1)
    goalMarking.set(places["on"], ProductColorLiteral(param_colors[2], [objects["b2"], objects["b1"]]), 1)
    goalMarking.set(places["on"], ProductColorLiteral(param_colors[2], [objects["b4"], objects["b5"]]), 1)
    goalMarking.set(places["on"], ProductColorLiteral(param_colors[2], [objects["b5"], objects["b3"]]), 1)

    return pn, initialMarking
