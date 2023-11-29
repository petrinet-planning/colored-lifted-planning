import argparse
import sys

from translation import translate_problem, test_validity


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument("pddl_domain_path", metavar="pddl_domain_path", type=str, nargs=1 )
    parser.add_argument("pddl_problem_path", metavar="pddl_problem_path", type=str, nargs=1 )
    parser.add_argument("pnml_output_path", metavar="pnml_output_path", type=str, nargs=1 )
    parser.add_argument("pnml_query_path", metavar="pnml_query_path", type=str, nargs=1 )

    parser.add_argument('--testValidity', dest='main_action', action='store_const',
                    const="validity", default="translation",
                    help="Output whether domain supports translation")
    
    args = parser.parse_args()


    if args.main_action == "translation":
        translate_problem(
            args.pddl_domain_path[0],
            args.pddl_problem_path[0],
            args.pnml_output_path[0],
            args.pnml_query_path[0]
        )
    elif  args.main_action == "validity":
        errorcode = test_validity(
            args.pddl_domain_path[0],
            args.pddl_problem_path[0]
        )
        exit(errorcode.statuscode)
    else:
        print("Unhandled main-action: " + args.main_action)


if __name__ == "__main__":
    main()