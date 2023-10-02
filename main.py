from unified_planning.io import PDDLReader
from unified_planning.model import Problem

import planning_to_petri
from blocksworldnet import pn, initialMarking
from petrinet.petrinet import PetriNet

reader = PDDLReader()
pddl_problem: Problem = reader.parse_problem('test_files/domain.pddl', 'test_files/p01.pddl')
print(pddl_problem)

generated_pn, generated_initial_marking = planning_to_petri.translate("generated_blocksworld", pddl_problem)


pnml = generated_pn.generate_pnml(generated_initial_marking)
with open("output.pnml", "w") as f:
    print(pnml, file=f)


