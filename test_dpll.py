# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
# sys.path.insert(1, r'F:\Documents\VU\KR\Sudoku_solver_group3')

from dpll import *
from draw_sudoku import *
from sudoku_heuristics import branching_heuristics_collection

full_problem = get_dimacs(sudoku_file_path=r'sud_examples/sudoku_2',
                          append_rules=True)

cnf = dimacs_to_cnf(full_problem)


initial_problem = dimacs_to_cnf(get_dimacs(sudoku_file_path=r'sud_examples/sudoku_2',
                          append_rules=False))

initial_problem = [item for sublist in initial_problem for item in sublist]

import time
now = time.time()
solution_dpll_negated_first = Solver(cnf)
print('ANSWER:')
print(solution_dpll_negated_first.solve())
print('--------------------------')

print('NUMBER OF ITERATIONS:')
print(solution_dpll_negated_first.iteration)

print('TIME TAKEN:')
print(time.time()-now)
print('-----------------------------')

# import time
now = time.time()
solution_dpll = Solver(cnf)
solution_dpll.negated_first=False
print('ANSWER:')
print(solution_dpll.solve())
print('--------------------------')

print('NUMBER OF ITERATIONS:')
print(solution_dpll.iteration)

print('TIME TAKEN:')
print(time.time()-now)


def test_heuristics():
    cnf_formula = [-111, -112], [-111, 122, 123, -112], [-111, 114, -112], [121, 123, -111], [-123, 144, -112], [
        -111], [144, 112], [112], [112, 156, 167, 111]
    random_heuristic = branching_heuristics_collection("RANDOM")
    lucky_literal = random_heuristic(cnf_formula)
    print("The lucky literal is ", lucky_literal)
    most_frequent_heuristic = branching_heuristics_collection("DLCS")
    most_frequent_combined = most_frequent_heuristic(cnf_formula)
    print("The most frequent combined sum literal is ", most_frequent_combined)
    assert most_frequent_combined == 112, "Most DLCS frequent (combined sum) literal is -112"
    most_frequent_heuristic = branching_heuristics_collection("DLIS")
    most_frequent_individual = most_frequent_heuristic(cnf_formula)
    assert most_frequent_individual == -111, "Most DLIS frequent (individual sum) literal is 111"
    print("The most frequent individual sum literal is ", most_frequent_individual)


test_heuristics()
# board = draw(filename='solution_negated_first')
# board.draw(solution_dpll_negated_first.sudoku_solution)
#
# board = draw(filename='solution_positive_first')
# board.draw(solution_dpll.sudoku_solution)
#
# board = draw(filename='original_problem')
# board.draw(initial_problem)