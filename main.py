import argparse
from sudoku_heuristics import heuristic_list
from dpll import run_dpll

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dimacs', help = 'Path to dimacs file for sudoku problem')
    parser.add_argument('rules', help = 'Path to rules file for Sudoku')
    parser.add_argument('-hr', '--hueristic',
                         help=f'Hueristic to be used with dpll. Options are: {heuristic_list}',
                         default='most_common_negative')
    parser.add_argument('-v', '--verbose',help='Print out dpll steps (not advisable with big problems)', type = bool,
                        default=False)


    args = parser.parse_args()
    run_dpll(problem_path = args.dimacs, hueristic = args.hueristic, rule_path =  args.rules,verbose= args.verbose)





if __name__ == "__main__":
    main()