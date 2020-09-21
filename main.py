import argparse
from sudoku_heuristics import heuristic_list
from dpll import run_dpll

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dimacs', help = 'Path to dimacs file for SAT problem')
    parser.add_argument('-r','--rules', help = 'Path to rules file for Sudoku. Not needed for other SAT problems')
    parser.add_argument('-hr', '--hueristic',
                         help=f'Hueristic to be used with dpll. Options are: {heuristic_list}',
                         default='DLCS')
    parser.add_argument('-v', '--verbose',help='Prints out dpll steps (not advisable with big problems)', type = bool,
                        default=False)
    parser.add_argument('-d', '--draw', help = 'Saves image of original problem and solved sudoku board. Only works with Sudoku SAT problem', type = bool, default= False)


    args = parser.parse_args()
    run_dpll(problem_path = args.dimacs, hueristic = args.hueristic, rule_path =  args.rules,verbose= args.verbose, draw=args.draw)





if __name__ == "__main__":
    main()
