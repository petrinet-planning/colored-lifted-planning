from unified_planning.io import PDDLReader
from blocksworldnet import pn


reader = PDDLReader()
pddl_problem = reader.parse_problem('test_files/domain.pddl', 'test_files/p01.pddl')
print(pddl_problem)





print(pn)
