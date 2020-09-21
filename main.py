import argparse
import sys
from sudoku_heuristics import heuristic_list
from dpll import run_dpll

def main():
    # SAT -Sn inputfile
    # for example: SAT -S2 sudoku_nr_10 ,
    # where SAT is the (compulsory) name of your program,
    # n=1 for the basic DP and n=2 or 3 for your two other strategies,
    # and the input file is the concatenation of all required input clauses (in your case: sudoku rules + given puzzle).

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help = 'Path to file with SAT problem encoded as CNF in DIMACS format')

    parser.add_argument('-hr', '--branching_heuristic',
                         help=f'Branching Heuristic to be used with DPLL. Options are: {heuristic_list}',
                         default='S1')

    parser.add_argument('-v', '--verbose',help='Prints out dpll steps (not advisable with big problems)', type = bool,
                        default=False)
    parser.add_argument('-d', '--draw', help = 'Saves image of original problem and solved sudoku board. '
                                               'Only works with Sudoku SAT problem', type = bool, default= False)

    args = parser.parse_args()

    heuristics_dict = {'S1': 'RANDOM',
                       'S2': 'DLIS_negated',
                       'S3': 'DLIS',
                       'S4': 'DLCS',
                       'S5': 'JEROSLOW_WANG',
                       'S6': 'JEROSLOW_WANG_TWO_SIDED'}

    branching_heuristic =  heuristics_dict[args.branching_heuristic]

    run_dpll(problem_path = args.input_file,
             heuristic= branching_heuristic,
             append_rules=False,
             verbose=args.verbose,
             draw=args.draw)

if __name__ == "__main__":
    main()
