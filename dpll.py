import itertools
import glob
import random
import time
import sudoku_heuristics
import draw_sudoku

def hasUnitClause(cnf):
    for clause in cnf:
        if len(clause) == 1:
                return(True)
        return False

class split:
    def __init__(self,cnf,literal,branch):
        pass

def run_dpll(problem_path, hueristic, rule_path = None,  verbose = False, draw=True):
    full_problem = get_dimacs(example_path=problem_path,
                          rules_path=rule_path)
    
    cnf = dimacs_to_cnf(full_problem)

    start = time.time()
    chosen_huerestic = sudoku_heuristics.branching_heuristics_collection(hueristic)
    solver = Solver(cnf, hueristic= chosen_huerestic)
    solver.debug_print = verbose
    print(f'SOlving DPLL with huerestic: {hueristic}')
    print('ANSWER:')
    print(solver.solve())
    print('--------------------------')
    print('NUMBER OF ITERATIONS:')
    print(solver.iteration)
    
    print('TIME TAKEN:')
    print(time.time()-start)
    print(f'Average clause-literal ratio over all executed branches: {solver.avg_ratio}')
    if draw:
        board = draw_sudoku.Draw()
        solved_board = f"{hueristic}.jpg"
        initial_board = f'{hueristic}_initial_problem.jpg'
        board.draw(solver.sudoku_solution,filename=solved_board)
        
        initial_problem = dimacs_to_cnf(get_dimacs(example_path=problem_path,
                                rules_path=None))

        initial_problem = [item for sublist in initial_problem for item in sublist] 
    
        # initial_board = draw_sudoku.Draw()
        board.draw(initial_problem,filename=initial_board)

        print(f'Solution output: {solved_board}\nInitial problem: {initial_board}')


class Solver:
    def __init__(self, cnf,
                 hueristic = sudoku_heuristics.getMostCommonLiteralNegative ):
        self.hueristic = hueristic
        self.sudoku_solution = []
        self.iteration = 0
        self.result = None
        self.avg_ratio = 0.0
        
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

        n_cnf = len(cnf)
        n_literal = len(literal)
        ratio = n_cnf / n_literal
        self.avg_ratio = self.avg_ratio + ratio
        if self.debug_print:
            print('unit clauses and pure literals processed')
            print('cnf')
            print(cnf)
            print('literals')
            print(literal)
            print(f'Current clause - literal ratio: {ratio}')

        solution = solution+current_selection
        #check trivial cases
        if [] in cnf:
            self.solution = list(set(solution))
            self.sudoku_solution = self.getSudokuSolution(list(set(solution)))
            self.result = False
            self.avg_ratio = self.avg_ratio / self.iteration
            return False
        if not cnf:
            self.solution = list(set(solution))
            self.sudoku_solution = self.getSudokuSolution(list(set(solution)))
            self.result = True
            self.avg_ratio = self.avg_ratio / self.iteration
            return True

        #select literal using chosen
        t=self.hueristic(cnf)
       
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
  '''Reads initial problem + rules of sudoku and outputs dimacs file containing rules + sudoku example'''

  sud_dimacs = open(example_path, 'r').read()

  rules_string = ''
   
  if rules_path:
    rules_string = open(rules_path, 'r').read()

  full_problem = sud_dimacs + rules_string 

  return full_problem


def sud_txt_to_dimacs(example_path='top95.sdk.txt'):
    '''This function reads .txt (txtfile one line of 81 characters per puzzle, '.' for free space)
    Translate txtfile to DIMACS. Puts Dimacs file in folder sud_examples
    top95.sdk.txt is a set of 95 "hard" puzzles, favoured benchmark set of a web forum for sudokus'''

    all_sudokus = open(example_path, 'r').read()
    all_sudokus = all_sudokus.split("\n")
    sudnr = 1

    for sudoku in all_sudokus:
        sud_file = open(r'C:\Users\Tim de Boer\Desktop\Coderen\Sudoku_solver_group3\Sudoku_solver_group3\sud_examples\sudoku_%d'%sudnr, 'w+')
        row = 1
        column = 1

        for place in sudoku:
            if place.isdigit():
                sud_file.write(str(row) + str(column) + str(place) + ' 0\n')   

            column += 1

            if column == 10:
                column = 1
                row += 1    
            
        sudnr += 1

    return all_sudokus
