import itertools
import glob
import random

def hasUnitClause(cnf):
    for clause in cnf:
        if len(clause) == 1:
                return(True)
        return False

class split:
    def __init__(self,cnf,literal,branch):
        pass

class Solver:
    def __init__(self, cnf):
        self.sudoku_solution = []
        self.iteration = 0
        self.negated_first=True
        #get clasuses in cnf form
        self.cnf=[list(i) for i in cnf]
        self.solution=[]
        #get literals
        self.literals = []
        for item in  self.cnf:
            for i in item:
                if i not in self.literals:
                    self.literals.append(i)
        self.debug_print = False

    def getSudokuSolution(self,solution):
        return([i for i in solution if i > 0])

    def solve(self):
        return self.dpll(self.cnf,self.literals)
        

    def dpll(self,cnf,literal, solution=[]):
        """
        Function implements dpll algo
        """
        #update and print branch number
        self.iteration+=1
        print(self.iteration, end = '\r')

        
 

        current_selection = []

        if self.debug_print:
            print('---------------------------')
            print('Initial Solution')
            print(solution)
            print('cnf')
            print(cnf)
            print('literals')
            print(literal)

        #Set all literals in unit clauses to true
        #Remove clauses that are true
        # Remove true literals from all clauses 
        for clause in cnf:
            if len(clause) == 1:
                cnf,literal,selected =self.unit_p(cnf, literal)
                current_selection.append(selected)

        if self.debug_print:
            print('unit clauses and pure literals processed')
            print('cnf')
            print(cnf)
            print('literals')
            print(literal)

        solution = solution+current_selection
        #check trivial cases
        if [] in cnf:
            self.solution = list(set(solution))
            self.sudoku_solution = self.getSudokuSolution(list(set(solution)))
            return False
        if not cnf:
            self.solution = list(set(solution))
            self.sudoku_solution = self.getSudokuSolution(list(set(solution)))
            return True

        #get the most common remaining literal (t) in cnf
        t=self.getMostCommonLiteral(cnf)
       
        if self.debug_print:
            print('selected literal')
            print(t)

        #update solutions
        negated_branch_solution =  list(set(solution+[-t]))
        
        solution = list(set(solution+[t]))
        # remove selected literal from list of literals
        if t in literal:
            literal.remove(t)
        
        #Split on t, try to solve the cnf with t and -t
        branch1,_=self.reduce(cnf,t)
        branch2,_=self.reduce(cnf,-t)

        if self.debug_print:
            print('branch')
            print(branch1,'||', branch2 )
            print('current solutions')
            print(solution, '||' ,negated_branch_solution)


        if self.negated_first:
            return(self.dpll(branch2,literal, solution=negated_branch_solution) or self.dpll(branch1,literal,solution=solution))
        else:
            return(self.dpll(branch1,literal, solution=solution) or self.dpll(branch2,literal,solution=negated_branch_solution))

    def unit_p(self,cnf,literal):
        """
        Function selects a literal from from cnf list that is a unit clause
        Reduces the cnf list with respect to selected literal
        (Check reduce function for explanation)
        removes selected literal from literal list
        return new cnf, literal list, selected literal
        """
        t1=0

        #check for a unit clause and add to list
        #select literal from unit clause (t1)
        unit_clauses = []
        _cnf = []
        for clause in cnf[::-1]:
            if len(clause)==1:
                t1=clause[0]
                break
        
        #reduce cnf with respect to literal (t1)
        _cnf, selected = self.reduce(cnf,t1)

        #remove that literal (t1) from literal list
        if t1 in literal:
            literal.remove(t1)
        if -t1 in literal:
            literal.remove(-t1)

        # return new cnf, literals, literals that were selected
        return (_cnf,literal, selected)
   
    def reduce(self,cnf,t):
        """
        Function takes in cnf and a literal t
        Assumes literal t is in a unit clause
        Sets literal t to true
        Remove all unit clauses that contain literal t
         Remove literal -t from all clauses
         returns new cnf and t
        """
        unit_clauses=[]

        # Remove all unit clauses that contain literal t
        _cnf =[]
        for clause in cnf:
            if t in clause:
                unit_clauses.append(clause)
            else:
                _cnf.append(clause)

        
        # Remove literal -t from all clauses
        for clause in cnf:
            if (t*-1) in clause:

                _cnf.remove(clause)
                _cnf.append([x for x in clause if x != -t])

        
        return _cnf,t
        
    
    def getMostCommonLiteral(self,cnf):
        """
        Finds and returns the literal that occurs the most in cnf
        """
        merged = list(itertools.chain(*cnf))    
        if len(merged)>0:
            return max(set(merged), key=merged.count)
        else:
            self.ou=True     



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


def get_dimacs(example_path='sudoku_example_DIMACS.txt', rules_path='sudoku_rules_DIMACS.txt'):
  
  '''This function reads sudoku9x9.txt (txtfile with 1000 9x9 sudoku's) and will translate it to DIMACS
  Every point in that file equals 0; every number is a given number in the sudoku
  So 1 9x9 sudoku are the first 81 characters in the file.
  It also reads the rules of sudoku as Dimacs

  Output of the function is a big dimacs file containing rules + sudoku example'''



  # we have 1 example Dimacs file from Canvas
  example_sud_dimacs = open(example_path, 'r').read()


  # load in the constraints / rules
  # (1 independent number in every place, 1 independent number in every row, every column and every square)
  rules_string = ''
  if rules_path:
    rules_string = open(rules_path, 'r').read()
  

  # rules_string is already in DIMACS, no need to change anything for it.
  # we want to solve a combination of the constraint with the given numbers of the sudoku with DPLL
  # so I think our cnf problem statement should be: rules + given_numbers
  # full_problem = rules_string + sudoku_given numbers
  # for the example sudoku:
  full_problem = example_sud_dimacs + rules_string

  return full_problem