import glob
import random
import dpll

# here we can call dpll, or GSAT, or Jeroslaw for our solution:
# currently, we only have a dpll function
# full_problem1 = dpll.get_dimacs(example_path=r'F:\Documents\VU\KR\Sudoku_solver_group3\sample.txt.txt',
#                           rules_path=None)
full_problem1 = dpll.get_dimacs(example_path=r'F:\Documents\VU\KR\Sudoku_solver_group3\sudoku_example_DIMACS.txt',
                          rules_path=r'F:\Documents\VU\KR\Sudoku_solver_group3\sudoku_rules_DIMACS.txt')
clauses1 = dpll.dimacs_to_cnf(full_problem1)
solution_dpll = dpll.Solver(clauses1)

#TODO: get the output sudoku..

# uncomment the line below to see that this gives as output True, so the sudoku is solved
# program is however sloooooow to give answer to this statement

import time
now = time.time()
print('ANSWER:')
print(solution_dpll.solve())
print('--------------------------')
print("SOLUTION:")
print(solution_dpll.solution, len(solution_dpll.solution) )
print('NUMBER OF ITERATIONS:')
print(solution_dpll.iteration)

print('TIME TAKEN:')
print(time.time()-now)



