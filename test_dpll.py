# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
# sys.path.insert(1, r'F:\Documents\VU\KR\Sudoku_solver_group3')

from dpll import *
from draw_sudoku import *

#sud_txt_to_dimacs(example_path=r"C:\Users\Tim de Boer\Desktop\Coderen\Sudoku_solver_group3\Sudoku_solver_group3\sudokus9x9.txt")
# txt files are already in the folders.

full_problem = get_dimacs(example_path=r'sud_examples\sudoku_2',
                          rules_path=r'sudoku_rules_DIMACS.txt')

cnf = dimacs_to_cnf(full_problem)


initial_problem = dimacs_to_cnf(get_dimacs(example_path=r'sud_examples\sudoku_2',
                          rules_path=None))

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

board = draw(filename='solution_negated_first')
board.draw(solution_dpll_negated_first.sudoku_solution)

board = draw(filename='solution_positive_first')
board.draw(solution_dpll.sudoku_solution)

board = draw(filename='original_problem')
board.draw(initial_problem)