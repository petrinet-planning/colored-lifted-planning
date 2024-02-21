from unified_planning.io import PDDLReader
from unified_planning.model import Problem, Action, OperatorKind, FNode
from .planning_to_petri_builder import get_arc_directions, PlanningToPetriBuilder, generate_goal_query_xml

class ValidityStatus(object):
    parserError: bool = False
    unsupportedInheritence: bool = False
    unsupportedRelationshipType: bool = False
    otherError: bool = False

    @property
    def success(self):
        return self.statuscode == 0

    @property
    def statuscode(self):
        return (
            0b0001 if self.parserError else 0 |
            0b0010 if self.unsupportedInheritence else 0 |
            0b0100 if self.unsupportedRelationshipType else 0 |
            0b1000 if self.otherError else 0 
        )


def test_validity(pddl_domain_path: str, pddl_problem_path: str) -> ValidityStatus:
    reader = PDDLReader()
    pddl_problem: Problem 

    try:
        pddl_problem: Problem = reader.parse_problem(pddl_domain_path, pddl_problem_path)
    except:
        status = ValidityStatus()
        status.parserError = True
        return status

    return test_problem_validity(pddl_problem)


def test_problem_validity(problem: Problem) -> ValidityStatus:
    status = ValidityStatus()

    status.unsupportedRelationshipType = not isValid_action_relationships(problem)
    if status.success:
        status.otherError = not can_translate(problem)

    return status


def isValid_action_relationships(problem: Problem) -> bool:
    for action in problem.actions:
        try:
            get_arc_directions(action)
        except:
            return False

    return True


def can_translate(problem: Problem) -> bool:
    try:
        builder = PlanningToPetriBuilder(problem)
        generated_pn = builder.generate_petrinet()
        generated_initial_marking = builder.generate_initial_marking()
        return True
    except:
        return False
