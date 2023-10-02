from petrinet import petrinet
from petrinet.arc import ArcPlaceToTransition, ArcTransitionToPlace
from petrinet.color import *
from petrinet.literal import EnumerationColorLiteral, DotColorLiteral, ProductColorLiteral
from petrinet.marking import Marking
from petrinet.place import Place
from petrinet.value import ProductColorValue
from petrinet.variable import *
from petrinet.transition import *
from petrinet.weighted_values import WeightedValues

pn = petrinet.PetriNet("Blocksworld_p01")

# Objects
dotColor = DotColor()
dotLiteral = DotColorLiteral(dotColor)
objectsColor = EnumerationColor("objects")
objects_b1 = objectsColor.add(EnumerationColorLiteral(objectsColor, "b1"))
objects_b2 = objectsColor.add(EnumerationColorLiteral(objectsColor, "b2"))
objects_b3 = objectsColor.add(EnumerationColorLiteral(objectsColor, "b3"))
objects_b4 = objectsColor.add(EnumerationColorLiteral(objectsColor, "b4"))
objects_b5 = objectsColor.add(EnumerationColorLiteral(objectsColor, "b5"))

# Predicates and Actions

# ParamColors
paramColors0 = pn.add_color(dotColor)
paramColors1 = pn.add_color(objectsColor)
paramColors2 = pn.add_color(ProductColor("params_2", [objectsColor, objectsColor]))

# Variables
var_ob = pn.add_variable(Variable("ob", objectsColor))
var_underob = pn.add_variable(Variable("underob", objectsColor))

# Predicates / Places
pred_clear = pn.add_place(Place("pred_clear", paramColors1))
pred_on_table = pn.add_place(Place("pred_on_table", paramColors1))
pred_arm_empty = pn.add_place(Place("pred_arm_empty", paramColors0))
pred_holding = pn.add_place(Place("pred_holding", paramColors1))
pred_on = pn.add_place(Place("pred_on", paramColors2))

# Actions / Transitions
# Pickup
act_pickup = pn.add_transition(Transition("act_pickup"))
pn.add_arc(ArcPlaceToTransition(pred_clear, act_pickup, {var_ob: 1}))          # delete
pn.add_arc(ArcPlaceToTransition(pred_on_table, act_pickup, {var_ob: 1}))       # delete
pn.add_arc(ArcPlaceToTransition(pred_arm_empty, act_pickup, {dotLiteral: 1}))  # delete
pn.add_arc(ArcTransitionToPlace(act_pickup, pred_holding, {var_ob: 1}))        # add

# Putdown
act_putdown = pn.add_transition(Transition("act_putdown"))
pn.add_arc(ArcTransitionToPlace(act_putdown, pred_clear, {var_ob: 1}))          # add
pn.add_arc(ArcTransitionToPlace(act_putdown, pred_on_table, {var_ob: 1}))       # add
pn.add_arc(ArcTransitionToPlace(act_putdown, pred_arm_empty, {dotLiteral: 1}))  # add
pn.add_arc(ArcPlaceToTransition(pred_holding, act_putdown, {var_ob: 1}))        # delete

# Stack
act_stack = pn.add_transition(Transition("act_stack"))
pn.add_arc(ArcPlaceToTransition(pred_clear, act_stack, {var_ob: 1}))          # require pred_clear
pn.add_arc(ArcTransitionToPlace(act_stack, pred_clear, {var_ob: 1}))
pn.add_arc(ArcTransitionToPlace(act_stack, pred_arm_empty, {dotLiteral: 1}))  # add pred_arm_empty
pn.add_arc(ArcPlaceToTransition(pred_holding, act_stack, {var_ob: 1}))        # delete pred_holding
pn.add_arc(ArcTransitionToPlace(act_stack, pred_on, {ProductColorValue(paramColors2, [var_ob, var_underob]): 1}))  # add pred_arm_empty

# Unstack
act_unstack = pn.add_transition(Transition("act_unstack"))
pn.add_arc(ArcTransitionToPlace(act_unstack, pred_clear, {var_ob: 1}))          # require pred_clear
pn.add_arc(ArcPlaceToTransition(pred_clear, act_unstack, {var_ob: 1}))
pn.add_arc(ArcPlaceToTransition(pred_arm_empty, act_unstack, {dotLiteral: 1}))  # delete pred_arm_empty
pn.add_arc(ArcTransitionToPlace(act_unstack, pred_holding, {var_ob: 1}))        # add pred_holding
pn.add_arc(ArcPlaceToTransition(pred_on, act_unstack, {ProductColorValue(paramColors2, [var_ob, var_underob]): 1}))  # del pred_arm_empty

# Markings
# Initial
initialMarking = Marking()
initialMarking.set(pred_clear, objects_b1, 1)
initialMarking.set(pred_clear, objects_b2, 1)
initialMarking.set(pred_clear, objects_b5, 1)
initialMarking.set(pred_on_table, objects_b3, 1)
initialMarking.set(pred_on_table, objects_b4, 1)
initialMarking.set(pred_on_table, objects_b5, 1)
initialMarking.set(pred_arm_empty, dotLiteral, 1)
initialMarking.set(pred_on, ProductColorLiteral(paramColors2, [objects_b1, objects_b4]), 1)
initialMarking.set(pred_on, ProductColorLiteral(paramColors2, [objects_b2, objects_b3]), 1)

# Goal
goalMarking = Marking()
initialMarking.set(pred_on, ProductColorLiteral(paramColors2, [objects_b1, objects_b4]), 1)
initialMarking.set(pred_on, ProductColorLiteral(paramColors2, [objects_b2, objects_b1]), 1)
initialMarking.set(pred_on, ProductColorLiteral(paramColors2, [objects_b4, objects_b5]), 1)
initialMarking.set(pred_on, ProductColorLiteral(paramColors2, [objects_b5, objects_b3]), 1)
