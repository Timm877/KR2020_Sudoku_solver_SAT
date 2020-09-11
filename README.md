# Sudoku solver group 3
[Link to google docs for tasks, research question and planning.](https://docs.google.com/document/d/1F_wTVEpV_9wb2ctD3C9XG-5DSfD8SNUY4EB0c1tK0Lg/edit?usp=sharing)

In main file (now called test_dpll), we have functions:
- dimacs_to_cnf which converts a dimacs file to a list with the cnf statement of that file.
- get_dimacs:   This function reads sudoku9x9.txt (txtfile with 1000 9x9 sudoku's) and will translate it to DIMACS.
              	Every point in that file equals 0; every number is a given number in the sudoku
                So the first 9x9 sudoku is made with the first 81 characters in the file.
                In this function, also the rules of sudoku from Canvas are loaded as Dimacs.
                Output of the function is a dimacs file containing rules + sudoku example; this Dimacs fils can be used as input for dimacs_to_cnf.
            
dpll.py is a file which takes as input a cnf statement, applies DPLL algorithm and (currently) only outputs True if SAT and False if UNSAT.
