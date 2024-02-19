import re
from enum import Enum

from unified_planning.model import Problem, Action, OperatorKind, FNode, types, InstantaneousAction

from petrinet import *
from petrinet.guard import *
from petrinet.guardex import *


class ArcDirections(Enum):
    UNHANDLED = -1
    NONE = 0b00
    PLACE_TO_TRANSITION = 0b01
    TRANSITION_TO_PLACE = 0b10
    BOTH = 0b11

class PlanningToPetriBuilder(object):
    pn: PetriNet
    problem: Problem

    dot_color: DotColor = DotColor()
    dot_literal: DotColorLiteral = DotColorLiteral(dot_color)
    type_colors: dict[str, EnumerationColor] = dict()
    type_literals: dict[str, EnumerationColorLiteral] = dict()
    param_colors: dict[str, Color] = dict()


    def __init__(self, problem: Problem):
        self.problem = problem


    def generate_petrinet(self) -> PetriNet:
        self.pn = PetriNet(self.problem.name)

        self.make_hierarchy()

        self.make_base_colors()
        self.make_places()
        self.make_transitions()
        self.connect_actions()
        self.make_guards()
        self.make_goal_transition()

        return self.pn

    def get_all_descendants(self, user_type, hierarchy):
        descendants = []
        children = hierarchy.get(user_type, [])

        for child in children:
            descendants.append(child.name)
            descendants.extend(self.get_all_descendants(child, hierarchy))
            
        return descendants
    

    def make_hierarchy(self):
        self.hierarchy = dict()
        for usertype in self.problem.user_types:
            self.hierarchy[usertype.name] = [obj.name for obj in self.problem.all_objects if obj.type.name == usertype.name or obj.type.name in self.get_all_descendants(usertype, self.problem.user_types_hierarchy)] # or obj.type.name in usertype.ancestors
    

    def make_base_colors(self):
        
        self.type_colors["object"] = EnumerationColor("object")

        #for usertype in self.problem.user_types:
        #    self.type_colors[usertype.name] = EnumerationColor(usertype.name)

        # self.type_colors[""] = DotColor()

        #todo: assumption, no 2 objects have the same name 

        for obj in self.problem.all_objects:
            self.type_literals[obj.name] = self.type_colors["object"].add(EnumerationColorLiteral(self.type_colors["object"], obj.name))


    def get_or_make_param_color(self, signature: list[types._UserType]) -> Color:
        param_color_name = "params" + "_".join(["object" for sig in signature])

        if param_color_name not in self.param_colors:
            if len(signature) == 0:
                self.param_colors[param_color_name] = self.pn.add_color(self.dot_color)
            elif len(signature) == 1: 
                self.param_colors[param_color_name] = self.pn.add_color(self.type_colors["object"])
            else:
                self.param_colors[param_color_name] = self.pn.add_color(ProductColor(param_color_name, [self.get_or_make_param_color(["object"]) for sig in signature]))

        return self.param_colors[param_color_name]


    variables: dict[tuple[str, str], EnumerationVariable] = dict()
    def get_or_make_variable(self, name: str, type_name: str):
        if (name, type_name) not in self.variables:
            self.variables[(name, type_name)] = self.pn.add_variable(EnumerationVariable(f"Var{name}_{type_name}", f"{name}:{type_name}", self.type_colors[type_name]))
            
        return self.variables[(name, type_name)]


    places: dict[str, Place] = dict()
    def make_places(self):
        for pred in self.problem.fluents:
            # places[pred.name] = pn.add_place(Place("pred_" + pred.name, param_colors[pred.arity]))
            self.places[pred.name] = self.pn.add_place(Place("pred_" + pred.name, self.get_or_make_param_color([arg.type for arg in pred.signature])))


    transitions: dict[str, Transition] = dict()
    def make_transitions(self):
        for action in self.problem.actions:
            self.transitions[action.name] = self.pn.add_transition(Transition(action.name))


    def _arg_to_value(self, arg: FNode, variables: dict[str, EnumerationVariable] = None) -> Value:
        if variables is not None:
            variable = variables.get(str(arg), None)

            if variable is not None:
                return variable
        
        return self.type_literals[str(arg)]


    def get_value(self, pred: FNode, variables: dict[str, EnumerationVariable] = None) -> Value:
        
        place = self.get_place(pred)
        color = place.color

        if type(color) is ProductColor:
            return ProductColorValue(color, [self._arg_to_value(arg, variables) for arg in pred.args])
        
        elif type(color) is EnumerationColor:
            return self._arg_to_value(pred.args[0], variables)

        elif type(color) is DotColor:
            return self.dot_literal
        
        else:
            raise "Unhandled color type"


    def get_value_literal(self, pred: FNode, variables: dict[str, EnumerationVariable] = None) -> Value:
        
        place = self.get_place(pred)
        color = place.color

        if type(color) is ProductColor:
            return ProductColorLiteral(color, [self._arg_to_value(arg, variables) for arg in pred.args])
        
        elif type(color) is EnumerationColor:
            return self._arg_to_value(pred.args[0], variables)

        elif type(color) is DotColor:
            return self.dot_literal
        
        else:
            raise "Unhandled color type"


    def connect_actions(self):

        for action in self.problem.actions:

            transition = self.transitions[action.name]
            variables = self.get_variables(action)

            for (pred, connection_type) in get_arc_directions(action).items():
                
                #To avoid it trying to create a place for non-predicate preconditions
                if pred.node_type is not (OperatorKind.NOT or OperatorKind.EQUALS):
                    place = self.get_place(pred)
                    weighted_values = dict([(self.get_value(pred, variables), 1)])

                # All 1 in planning
                #weighted_values: dict(EnumerationVariable, Literal[1]) = dict([(variables[arg.parameter().name], 1) for arg in pred.args])
                # weighted_values = dict([(variables[arg.parameter().name], 1) for arg in pred.args])
                
                def parse_pre_guard(node):
                    # Base case
                    if node.node_type is OperatorKind.PARAM_EXP:
                        return GuardExpression(value=self.get_or_make_variable(f'{node}', "object"))
                    
                    # Recursive cases
                    if node.node_type is OperatorKind.EQUALS:
                        return GuardExpression(op="eq", left=parse_pre_guard(node.args[0]), right=parse_pre_guard(node.args[1]))

                    elif node.node_type is OperatorKind.NOT:
                        return GuardExpression(op="!", left=parse_pre_guard(node.args[0]))

                if connection_type == ArcDirections.NONE:
                    raise "None-connection - Should never have left the get_arc_directions function"
                
                #Add the preconditions of form !(x = y) or (x = y) to the guard of the transition
                elif pred.node_type is OperatorKind.NOT or pred.node_type is OperatorKind.EQUALS:
                    if transition.guardex is None:
                        transition.guardex = parse_pre_guard(pred)
                    else:
                        transition.guardex = GuardExpression(op="and", left=parse_pre_guard(pred), right=transition.guardex)

                    
                elif connection_type == ArcDirections.PLACE_TO_TRANSITION:
                    self.pn.add_arc(ArcPlaceToTransition(place, transition, weighted_values))

                elif connection_type == ArcDirections.TRANSITION_TO_PLACE:
                    self.pn.add_arc(ArcTransitionToPlace(transition, place, weighted_values))

                elif connection_type == ArcDirections.BOTH:
                    self.pn.add_arc(ArcPlaceToTransition(place, transition, weighted_values))
                    self.pn.add_arc(ArcTransitionToPlace(transition, place, weighted_values))

                elif connection_type == ArcDirections.UNHANDLED:
                    raise "Unhandled connection type"
            
                else:
                    raise "Unhandled case"
                    
    def make_guards(self):
        for action in self.problem.actions:
            transition = self.transitions[action.name]
            for param in action.parameters:
                variable = self.get_or_make_variable(param.name, "object")
                if transition.guardex is None:
                    transition.guardex = GuardExpression.build_guard(self.hierarchy[param.type.name], variable)
                else:
                    transition.guardex = GuardExpression(op="and", left=GuardExpression.build_guard(self.hierarchy[param.type.name], variable), right=transition.guardex)


    def get_place(self, pred: FNode):
        place = self.places[pred.fluent().name]
        
        return place


    def get_variables(self, action: InstantaneousAction) -> dict[str, EnumerationVariable]:
        variables = dict([(param.name, self.get_or_make_variable(param.name, "object")) for param in action.parameters])

        return variables


    def generate_initial_marking(self) -> Marking:
        initialMarking = Marking()

        for pred, truth in self.problem.initial_values.items():
            if str(truth) != "true":
                continue

            place = self.get_place(pred)
            value = self.get_value_literal(pred)

            initialMarking.set(place, value, 1)

        return initialMarking


    def make_goal_transition(self):
        goalMarking = Marking()

        if (self.problem.goals[0].node_type is OperatorKind.AND):
            for pred in self.problem.goals[0].args:
                place = self.get_place(pred)
                value = self.get_value_literal(pred)

                goalMarking.set(place, value, 1)
        else:
            pred = self.problem.goals[0]
            place = self.get_place(pred)
            value = self.get_value_literal(pred)

            goalMarking.set(place, value, 1)

        goal = self.pn.add_transition(Transition("goal"))
        for place, values in goalMarking.values.items():
            self.pn.add_arc(ArcPlaceToTransition(place, goal, values))



def get_arc_directions(action) -> dict[FNode, ArcDirections]:

    in_pre = 0b100
    in_del = 0b010
    in_add = 0b001
    occurrences: dict[FNode, int] = {}

    if action.preconditions[0].node_type is OperatorKind.FLUENT_EXP:
        pred = action.preconditions[0]
        occurrences[pred] = occurrences.get(pred, 0) | in_pre
    elif action.preconditions[0].node_type is OperatorKind.AND:  # Only one precondition
        for pred in action.preconditions[0].args:
            occurrences[pred] = occurrences.get(pred, 0) | in_pre
    else:
        raise "Unhandled pred type"

    for eff in action.effects:
        if str(eff.value) == "true":
            occurrences[eff.fluent] = occurrences.get(eff.fluent, 0) | in_add
        else:
            occurrences[eff.fluent] = occurrences.get(eff.fluent, 0) | in_del

    occurrence_types: [int, PlanningToPetriBuilder.arc_directions] = dict()
    occurrence_types[in_pre | in_del | in_add] = ArcDirections.BOTH # "requires"
    occurrence_types[in_pre | in_del |      0] = ArcDirections.PLACE_TO_TRANSITION # "deletes"
    occurrence_types[in_pre |      0 | in_add] = ArcDirections.BOTH # "requires"
    occurrence_types[in_pre |      0 |      0] = ArcDirections.BOTH # "requires"
    occurrence_types[     0 | in_del | in_add] = ArcDirections.TRANSITION_TO_PLACE # "adds"
    occurrence_types[     0 | in_del |      0] = ArcDirections.UNHANDLED # "UNSUPPORTED"  # todo: Occurs in snake benchmark
    occurrence_types[     0 |      0 | in_add] = ArcDirections.TRANSITION_TO_PLACE # "adds"
    occurrence_types[     0 |      0 |      0] = ArcDirections.NONE # "not in"

    # Check validity
    for pred, occ in occurrences.items():
        if occurrence_types[occ] == ArcDirections.UNHANDLED: #"UNSUPPORTED":
            raise Exception("Unsupported predicate type - del without pre")
        if occurrence_types[occ] == ArcDirections.NONE: #"not in":
            raise Exception("Should not happen - pred exists, but doesn't")

    return dict([(pred, occurrence_types[type_id]) for pred, type_id in occurrences.items()])



def generate_goal_query_xml():
    return """\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<property-set xmlns="http://tapaal.net/">
  
  <property>
    <id>Goal Transition Reachable</id>
    <description>Goal Transition Reachable</description>
    <formula>
      <exists-path>
        <finally>
          <is-fireable>
            <transition>goal</transition>
          </is-fireable>
        </finally>
      </exists-path>
    </formula>
  </property>
</property-set>
"""
