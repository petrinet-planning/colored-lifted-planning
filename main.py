import argparse

from translation import translate_problem


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument("pddl_domain_path", metavar="pddl_domain_path", type=str, nargs=1 )
    parser.add_argument("pddl_problem_path", metavar="pddl_problem_path", type=str, nargs=1 )
    parser.add_argument("pnml_output_path", metavar="pnml_output_path", type=str, nargs=1 )
    parser.add_argument("pnml_query_path", metavar="pnml_query_path", type=str, nargs=1 )

    args = parser.parse_args()

    translate_problem(
        args.pddl_domain_path[0],
        args.pddl_problem_path[0],
        args.pnml_output_path[0],
        args.pnml_query_path[0]
    )

if __name__ == "__main__":
    main()