from unified_planning.io import PDDLReader
from unified_planning.model import Problem
from translation.planning_to_petri_builder import PlanningToPetriBuilder, generate_goal_query_xml
import time


def translate_problem(
        pddl_domain_path: str,
        pddl_problem_path: str = None,
        pnml_output_path: str = "output.pnml",
        pnml_query_path: str = "query.xml"
):
    reader = PDDLReader()
    pddl_problem: Problem = reader.parse_problem(pddl_domain_path, pddl_problem_path)

    builder = PlanningToPetriBuilder(pddl_problem)

    start_time = time.time()
    generated_pn = builder.generate_petrinet()
    end_time = time.time()
    print(f"Generated Petri net in {end_time - start_time} seconds")

    start_time = time.time()
    generated_initial_marking = builder.generate_initial_marking()
    end_time = time.time()
    print(f"Generated initial marking in {end_time - start_time} seconds")

    start_time = time.time()
    pnml = generated_pn.generate_pnml(generated_initial_marking)
    end_time = time.time()
    print(f"Generated PNML in {end_time - start_time} seconds")

    start_time = time.time()
    with open(pnml_output_path, "w") as f:
        print(pnml, file=f)
    end_time = time.time()
    print(f"Saved PNML to {pnml_output_path} in {end_time - start_time} seconds")

 
    with open(pnml_query_path, "w") as f:
        print(generate_goal_query_xml(), file=f)
