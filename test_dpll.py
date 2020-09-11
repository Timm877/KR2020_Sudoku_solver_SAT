import glob
import random
import dpll

def dimacs_to_cnf(full_problem):
  '''This function converts a dimacs file to a cnf statement'''

  clauses = []
  lines = full_problem.split("\n")
  for line in lines:
    if len(line) == 0 or line[0] in ['c', 'p', '%', '0']:
      continue
    clause = [int(x) for x in line.split()[0:-1]]
    clauses.append({x for x in clause})
  return clauses


def get_dimacs():
  
  '''This function reads sudoku9x9.txt (txtfile with 1000 9x9 sudoku's) and will translate it to DIMACS
  Every point in that file equals 0; every number is a given number in the sudoku
  So 1 9x9 sudoku are the first 81 characters in the file.
  It also reads the rules of sudoku as Dimacs

  Output of the function is a big dimacs file containing rules + sudoku example'''

  # Get the first sudoku out of the txt file with 1000 9x9 sudoku's 
  sudokus_9x9_string = open('sudokus9x9.txt', 'r').read()
  first_sudoku = sudokus_9x9_string[:81]

  #convert first_sudoku string into dimacs format
  #for every ., make a line with [rownum colnum 0 0]
  # for every number, make a line with [rownum colnum number 0]

  dimacs_sudoku = ''
  counter = 0
  for row in range(1,10):
    for column in range(1,10):  
      if first_sudoku[counter].isdigit() == True:
        dimacs_sudoku += (str(row) + ' ' +  str(column) + ' ' + first_sudoku[counter]  + ' 0\n')  
      else:
        dimacs_sudoku += (str(row) + ' ' +  str(column) + ' 0 0\n')
      counter +=1 
  print(dimacs_sudoku)   


  # we have 1 example Dimacs file from Canvas
  example_sud_dimacs = open('sudoku_example_DIMACS.txt', 'r').read()


  # load in the constraints / rules
  # (1 independent number in every place, 1 independent number in every row, every column and every square)
  rules_string = open('sudoku_rules_DIMACS.txt', 'r').read()
  

  # rules_string is already in DIMACS, no need to change anything for it.
  # we want to solve a combination of the constraint with the given numbers of the sudoku with DPLL
  # so I think our cnf problem statement should be: rules + given_numbers
  # full_problem = rules_string + sudoku_given numbers
  # for the example sudoku:
  full_problem = example_sud_dimacs + rules_string

  return full_problem



# here we can call dpll, or GSAT, or Jeroslaw for our solution:
# currently, we only have a dpll function
full_problem1 = get_dimacs()
clauses1 = dimacs_to_cnf(full_problem1)
solution_dpll = dpll.Solver(clauses1)

#TODO: get the output sudoku..

# uncomment the line below to see that this gives as output True, so the sudoku is solved
# program is however sloooooow to give answer to this statement
#print(solution_dpll.solve() == True)






