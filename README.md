# Sudoku solver group 3
[Link to google docs for tasks, research question and planning.](https://docs.google.com/document/d/1F_wTVEpV_9wb2ctD3C9XG-5DSfD8SNUY4EB0c1tK0Lg/edit?usp=sharing)

In main file (now called test_dpll), we have functions:
- dimacs_to_cnf which converts a dimacs file to a list with the cnf statement of that file.
- get_dimacs:   opens and reads problem file and rule file
                If you want to try a new problem with no rules, you can set rule_path to None

            
dpll.py is a file which takes as input a cnf statement, applies DPLL algorithm and (currently) only outputs True if SAT and False if UNSAT.

# Usage:


#read files and convert to cnf

full_problem1 = dpll.get_dimacs(example_path=r'F:\Documents\VU\KR\Sudoku_solver_group3\sudoku_example_DIMACS.txt',
                          rules_path=r'F:\Documents\VU\KR\Sudoku_solver_group3\sudoku_rules_DIMACS.txt')
clauses1 = dpll.dimacs_to_cnf(full_problem1)


#instantiate solver

solution_dpll = dpll.Solver(clauses1)

#Run solver

answer = solution_dpll.solve()

solution_dpll.iteration gives the number of iterations taken to reach the solution

solution_dpll.solution outputs the solution as a list of literals


solution_dpll.debug_flag = True will print out step by step information about the solver

solution_dpll.negated_first = True will compute the branch with negated literal fist
Example: if dpll splits on literal t, then it will solve the branch with -t first

Check notebook in notebooks folder for a better demonstration