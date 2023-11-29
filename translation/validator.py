from unified_planning.io import PDDLReader
from unified_planning.model import Problem, Action, OperatorKind, FNode

from .planning_to_petri_builder import get_arc_directions

class ValidityStatus(object):
    parserError: bool = False
    unsupportedInheritence: bool = False
    unsupportedRelationshipType: bool = False

    @property
    def success(self):
        return self.statuscode == 0

    @property
    def statuscode(self):
        return (
            0b001 if self.parserError else 0 |
            0b010 if self.unsupportedInheritence else 0 |
            0b100 if self.unsupportedRelationshipType else 0 
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

    status.unsupportedInheritence = not isValid_inheritence(problem)
    status.unsupportedRelationshipType = not isValid_action_relationships(problem)

    return status


def isValid_inheritence(problem: Problem) -> bool:
    for type in problem.user_types:
        if len(list(type.ancestors)) > 1:
            return False
    
    return True


def isValid_action_relationships(problem: Problem) -> bool:
    for action in problem.actions:
        try:
            get_arc_directions(action)
        except:
            return False

    return True

