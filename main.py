from unified_planning.io import PDDLReader
from unified_planning.model import Problem

from .translation import translate, generate_goal_query_xml


def translate_problem(
        pddl_domain_path: str,
        pddl_problem_path: str = None,
        pnml_output_path: str = "output.pnml",
        pnml_query_path: str = "query.xml"
):
    reader = PDDLReader()
    pddl_problem: Problem = reader.parse_problem(pddl_domain_path, pddl_problem_path)

    generated_pn, generated_initial_marking = translate(pddl_problem)

    pnml = generated_pn.generate_pnml(generated_initial_marking)
    with open(pnml_output_path, "w") as f:
        print(pnml, file=f)

    with open(pnml_query_path, "w") as f:
        print(generate_goal_query_xml(), file=f)
