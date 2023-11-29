from unified_planning.io import PDDLReader
from unified_planning.model import Problem
from translation.planning_to_petri_builder import PlanningToPetriBuilder, generate_goal_query_xml


def translate_problem(
        pddl_domain_path: str,
        pddl_problem_path: str = None,
        pnml_output_path: str = "output.pnml",
        pnml_query_path: str = "query.xml"
):
    reader = PDDLReader()
    pddl_problem: Problem = reader.parse_problem(pddl_domain_path, pddl_problem_path)

    builder = PlanningToPetriBuilder(pddl_problem)

    generated_pn = builder.generate_petrinet()
    generated_initial_marking = builder.generate_initial_marking()

    pnml = generated_pn.generate_pnml(generated_initial_marking)
    with open(pnml_output_path, "w") as f:
        print(pnml, file=f)

    with open(pnml_query_path, "w") as f:
        print(generate_goal_query_xml(), file=f)
