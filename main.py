import argparse
import sys
from sudoku_heuristics import heuristic_list
from dpll import run_dpll

def main():
    # You are free to choose any programming language you fancy, but we must be able to run your SAT solver with the command
    # SAT -Sn inputfile
    # for example: SAT -S2 sudoku_nr_10 ,
    # where SAT is the (compulsory) name of your program,
    # n=1 for the basic DP and n=2 or 3 for your two other strategies,
    # and the input file is the concatenation of all required input clauses (in your case: sudoku rules + given puzzle).
    parser = argparse.ArgumentParser()
    parser.add_argument('dimacs_cnf_file', help = 'Path to file with SAT problem encoded as CNF in DIMACS format')
    parser.add_argument('-r','--rules', help = 'Path to Sudoku rules file, encoded as CNF in DIMACS format. '
                                               'Not needed for other SAT problems')
    parser.add_argument('-hr', '--branching_heuristic',
                         help=f'Branching Heuristic to be used with DPLL. Options are: {heuristic_list}',
                         default='RANDOM')
    parser.add_argument('-v', '--verbose',help='Prints out dpll steps (not advisable with big problems)', type = bool,
                        default=False)
    parser.add_argument('-d', '--draw', help = 'Saves image of original problem and solved sudoku board. '
                                               'Only works with Sudoku SAT problem', type = bool, default= False)

    args = parser.parse_args()

    run_dpll(problem_path = args.dimacs_cnf_file,
             heuristic= args.branching_heuristic,
             append_rules=False,
             verbose= args.verbose, draw=args.draw)

if __name__ == "__main__":
    main()
