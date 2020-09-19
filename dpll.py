import itertools
import glob
import random
import time
import sudoku_heuristics
import draw_sudoku
import statistics
from collections import Counter
from copy import deepcopy

def get_all_modes(a):
    c = Counter(a)  
    mode_count = max(c.values())
    mode = {key for key, count in c.items() if count == mode_count}
    return list(mode)[0]

def hasUnitClause(cnf):
    for clause in cnf:
        if len(clause) == 1:
                return(True)
        return False

class split:
    def __init__(self,cnf,literal,branch):
        pass

def run_dpll(problem_path, hueristic, rule_path = None,  verbose = False, draw=False, show_stats=True):
    full_problem = get_dimacs(example_path=problem_path,
                          rules_path=rule_path)
    
    cnf = dimacs_to_cnf(full_problem)

    if show_stats:
        start = time.time()
    chosen_huerestic = sudoku_heuristics.branching_heuristics_collection(hueristic)
    solver = Solver(cnf, hueristic= chosen_huerestic)
    solver.debug_print = verbose
    
    if show_stats:
        print(f'SOlving DPLL with huerestic: {hueristic}')
    
    solver.solve()
    stats = solver.getRelevantStats()
    if show_stats:
        print('ANSWER:')
        print(solver.result)
        print('--------------------------')
        print('NUMBER OF ITERATIONS:')
        print(solver.iteration)
        
        print('TIME TAKEN:')
        print(time.time()-start)
        print('Relevant Statistics:')
        print(stats)
    
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

    return(solver,solver.result,stats)

class Solver:
    def __init__(self, cnf,
                 hueristic = sudoku_heuristics.getMostCommonLiteralNegative ):
        # print('Initializing')
        self.hueristic = hueristic
        self.sudoku_solution = []
        self.iteration = 0
        self.result = None
        self.stats = {
            'n_cnf': [],
            'n_literal' : [],
            'n_ratio': [],

            'avg_n_cnf': 0.0,
            'avg_n_literal': 0.0,
            'avg_n_ratio': 0.0,

            'mode_n_cnf': 0.0,
            'mode_n_literal': 0.0,
            'mode_n_ratio': 0.0,

            'median_n_cnf':0.0,
            'median_n_literal': 0.0,
            'median_n_ratio': 0.0,

            'ratio_of_avgs': 0.0,
            'ratio_of_modes':0.0,
            'ratio_of_medians': 0.0
   
        }

        self.relevant_stats = [
            'n_iterations',
            'initial_n_cnf',
            'initial_n_literal',
            'avg_n_cnf',
            'avg_n_literal',
            'avg_n_ratio',
            'mode_n_cnf',
            'mode_n_literal',
            'mode_n_ratio',
            'median_n_cnf',
            'median_n_literal',
            'median_n_ratio',
            'ratio_of_avgs',    
            'ratio_of_modes',
            'ratio_of_medians'        
        ]
        
        #get clasuses in cnf form
        self.cnf=[list(i) for i in cnf]
        self.solution=[]
        #get literals
        self.literals = [item for sublist in self.cnf for item in sublist] 
        # for item in  self.cnf:
        #     for i in item:
        #         if i not in self.literals:
        #             self.literals.append(i)
        self.debug_print = False
        self.stats['initial_n_cnf'] = len(self.cnf)
        self.stats['initial_n_literal'] = len(self.literals)

    def getRelevantStats(self):
        _dict = {}
        for key in self.relevant_stats:
            _dict[key] = self.stats[key]
        return(_dict)
        

    def getSudokuSolution(self,solution):
        return([i for i in solution if i > 0])

    def solve(self):
        return self.dpll(self.cnf)
        
    def collateResults(self, answer, solution):

        print('', end='\r')
        # iterations = self.iteration
        self.solution = list(set(solution))
        self.sudoku_solution = self.getSudokuSolution(list(set(solution)))
        self.result = answer

        self.stats['n_iterations'] = self.iteration
        if self.stats['n_cnf']:
            self.stats['avg_n_cnf'] = statistics.mean(self.stats['n_cnf'])
            self.stats['mode_n_cnf'] = get_all_modes(self.stats['n_cnf'])
            self.stats['median_n_cnf'] = statistics.median(self.stats['n_cnf'])

            self.stats['avg_n_literal'] = statistics.mean(self.stats['n_literal'])
            self.stats['mode_n_literal'] = get_all_modes(self.stats['n_literal'])
            self.stats['median_n_literal'] = statistics.median(self.stats['n_literal'])


            self.stats['avg_n_ratio'] = statistics.mean(self.stats['n_ratio'])
            self.stats['mode_n_ratio'] = get_all_modes(self.stats['n_ratio'])
            self.stats['median_n_ratio'] = statistics.median(self.stats['n_ratio'])

            try:
                self.stats['ratio_of_avgs'] = self.stats['avg_n_cnf'] / self.stats['avg_n_literal']
            except ZeroDivisionError:
                self.stats['ratio_of_avgs'] = None
            try:
                self.stats['ratio_of_modes'] = self.stats['mode_n_cnf'] / self.stats['mode_n_literal']
            except ZeroDivisionError:
                self.stats['ratio_of_modes'] = None
            try:
                self.stats['ratio_of_medians'] = self.stats['median_n_cnf'] / self.stats['median_n_literal'] 
            except ZeroDivisionError:
                self.stats['ratio_of_medians'] = None
            
    def updateStats(self, cnf):
        
        literal=list(set([item for sublist in cnf for item in sublist] ))
        n_cnf = len(cnf)
        n_literal = len(literal)
        ratio = n_cnf / n_literal
        self.stats['n_cnf'].append(n_cnf)
        self.stats['n_literal'].append(n_literal)
        self.stats['n_ratio'].append(ratio)


    def dpll(self,cnf, solution=[]):
        # self.updateStats(cnf,literal)
        # #check trivial cases
        # if [] in cnf:
        #     self.collateResults(False, solution)
        #     return False
        # if not cnf:
        #     self.collateResults(True, solution)
        #     return True
        """
        Function implements dpll algo
        """
        #update and print branch number
        self.iteration+=1
        print(f'Iteration number: {self.iteration}', end = '\r')

        


        current_selection = []

        if self.debug_print:
            print('---------------------------')
            print('Initial Solution')
            print(solution)
            print('cnf')
            print(cnf)


        #Set all literals in unit clauses to true
        #Remove clauses that are true
        # Remove true literals from all clauses 
        # while self.unitClauseExists(cnf):
        #         cnf,literal,selected =self.unitPropogation(cnf, literal)
        #         current_selection.append(selected)

        #Remove tautology
        cnf = self.removeTautology(cnf)
        
        #Do unit propogation
        cnf,selected =self.unitPropogation(cnf)
        current_selection = current_selection+selected  

        #set pure literals to true
        cnf,_selected =self.setPureLiteral(cnf)
        current_selection = current_selection+_selected   
        # print(literal == list(set([item for sublist in cnf for item in sublist] )))
       
        if self.debug_print:
            print('unit clauses and pure literals processed')
            print('cnf')
            print(cnf)

            # print(f'Current clause - literal ratio: {ratio}')

        solution = solution+current_selection
        #check trivial cases
        if [] in cnf:
            self.collateResults(False, solution)
            return False
        if not cnf:
            self.collateResults(True, solution)
            return True

        self.updateStats(cnf)
        #select literal using chosen
        t=self.hueristic(cnf)
       
        if self.debug_print:
            print('selected literal')
            print(t)

        #update solutions
        negated_branch_solution =  list(set(solution+[-t]))
        
        solution = list(set(solution+[t]))
        # remove selected literal from list of literals
        # literal_1 = literal
        # literal_2 = deepcopy(literal) 

        # if t in literal_1:
        #     literal_1.remove(t)

        # if -t in literal_2:
        #     literal_2.remove(-t)
        
        #Split on t, try to solve the cnf with t and -t
        branch1,_=self.reduce(cnf,t)
        branch2,_=self.reduce(cnf,-t)

        if self.debug_print:
            print('branch')
            print(branch1,'||', branch2 )
            print('current solutions')
            print(solution, '||' ,negated_branch_solution)


       
        return(self.dpll(branch1, solution=solution) or self.dpll(branch2,solution=negated_branch_solution))

    def unitClauseExists(self,cnf):
        for clause in cnf:
            if len(clause)==1:
                return True
        return False

    def unitPropogation(self,cnf):
        """
        Set all litreal in unit clauses to true
        Do unit propogation
        """
        selected = []
        while self.unitClauseExists(cnf):
            t1=0

            #check for a unit clause and add to list
            #select literal from unit clause (t1)
            # unit_clauses = []
            _cnf = []
            for clause in cnf[::-1]:
                if len(clause)==1:
                    t1=clause[0]
                    break
            
            #reduce cnf with respect to literal (t1)
            cnf, t1 = self.reduce(cnf,t1)
            selected.append(t1)
            #remove that literal (t1) from literal list
            # if t1 in literal:
            #     literal.remove(t1)


            # return new cnf, literals, literals that were selected
        return (cnf, selected)
   
    def reduce(self,cnf,t):
        """
        Assumes literal t is true
        does unit propogation after setting t to true
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

        # if t in literal:
        #         literal.remove(t)
        
        return _cnf,t
        
    def isTautology(self,clause):
        for literal in clause:
            if -literal in clause:
                return(True)
        return(False)    
    
    def removeTautology(self,cnf):
        for clause in cnf:
            # t = isTautology(clause):
            if self.isTautology(clause):
                cnf.remove(clause)
        # literal = list(set([item for sublist in cnf for item in sublist] ))
        return(cnf)


    def setPureLiteral(self,cnf):
        literal = list(set([item for sublist in cnf for item in sublist] ))
        selection = []
        
        for t in literal:
            if not -t in literal:
                cnf, selected = self.reduce(cnf,t)
                selection.append(selected)
        # literal = list(set([item for sublist in cnf for item in sublist] ))
        # print(literal == list(set([item for sublist in cnf for item in sublist] )))
        return(cnf,selection)


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