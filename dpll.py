import time

import draw_sudoku
import sudoku_heuristics
import statistics
from collections import Counter


def run_dpll(problem_path, rules_path, heuristic="RANDOM", verbose=False, draw=False, show_stats=True):
    full_problem = get_dimacs(problem_path, rules_path)
    cnf = dimacs_to_cnf(full_problem)

    if show_stats:
        start = time.time()

    chosen_heuristic = sudoku_heuristics.branching_heuristics_collection(heuristic)

    solver = Solver(cnf, heuristic=chosen_heuristic)
    solver.debug_print = verbose

    if show_stats:
        print(f'Solving DPLL with heuristic: {heuristic}')

    solver.solve()
    stats = solver.getRelevantStats()

    if show_stats:
        print_statistics(solver, start, stats)

    if verbose:
        print('Solution:\n', solver.solution)

    output_file_name = f"{problem_path.strip('.txt')}_{heuristic}.out"
    print(f'Solved DIMACS stored at: {output_file_name}')
    #    draw_sudoku_board(heuristic, problem_path, solver)
    # print 
    with open(output_file_name , 'w') as file_handle:
        if solver.result:
            file_handle.writelines("%s 0\n" % place for place in solver.solution)
        else: file_handle.write("")

    if draw:
        draw_sudoku_board(heuristic, problem_path, solver)

    return solver, solver.result, stats


def get_all_modes(a):
    c = Counter(a)
    mode_count = max(c.values())
    mode = {key for key, count in c.items() if count == mode_count}
    return list(mode)[0]


def has_unit_clause(cnf):
    for clause in cnf:
        if len(clause) == 1:
            return (True)
        return False


class split:
    def __init__(self, cnf, literal, branch):
        pass


def draw_sudoku_board(heuristic, problem_path, solver):
    board = draw_sudoku.Draw()
    solved_board = f"{problem_path.strip('.txt')}_{heuristic}.jpg"
    initial_board = f"{problem_path.strip('.txt')}_{heuristic}_initial_problem.jpg"
    board.draw(solver.sudoku_solution, filename=solved_board)
    initial_problem = dimacs_to_cnf(get_dimacs(sudoku_file_path = problem_path,
                                               rules_path=None))
    initial_problem = [item for sublist in initial_problem for item in sublist]
    # initial_board = draw_sudoku.Draw()
    board.draw(initial_problem, filename=initial_board)
    print(f'Solution output: {solved_board}\nInitial problem: {initial_board}')


def print_statistics(solver, start, stats):
    print('ANSWER: \n', solver.result)
    print('--------------------------')
    print('NUMBER OF ITERATIONS: \n', solver.iteration)
    print('TIME TAKEN:\n', time.time() - start)
    print('Relevant Statistics: \n', stats)


def debug_print_solution(cnf, solution):
    print('---------------------------')
    print('Initial Solution')
    print(solution)
    print('cnf')
    print(cnf)


class Solver:
    def __init__(self, cnf,
                 heuristic=sudoku_heuristics.most_common_literal_negative):
        # print('Initializing')
        self.heuristic = heuristic
        self.sudoku_solution = []
        self.iteration = 0
        self.result = None
        self.stats = {
            'n_cnf': [],
            'n_literal': [],
            'n_ratio': [],

            'avg_n_cnf': 0.0,
            'avg_n_literal': 0.0,
            'avg_n_ratio': 0.0,

            'mode_n_cnf': 0.0,
            'mode_n_literal': 0.0,
            'mode_n_ratio': 0.0,

            'median_n_cnf': 0.0,
            'median_n_literal': 0.0,
            'median_n_ratio': 0.0,

            'ratio_of_avgs': 0.0,
            'ratio_of_modes': 0.0,
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

        # get clasuses in cnf form
        self.cnf = [list(i) for i in cnf]
        self.solution = []
        # get literals
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
        return (_dict)

    def getSudokuSolution(self, solution):
        return ([i for i in solution if i > 0])

    def solve(self):
        return self.dpll(self.cnf)

    def collate_results(self, answer, solution):

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

    def update_stats(self, cnf):

        literal = list(set([item for sublist in cnf for item in sublist]))
        n_cnf = len(cnf)
        n_literal = len(literal)
        ratio = n_cnf / n_literal
        self.stats['n_cnf'].append(n_cnf)
        self.stats['n_literal'].append(n_literal)
        self.stats['n_ratio'].append(ratio)

    def dpll(self, cnf, solution=[]):

        self.iteration += 1
        print(f'Iteration number: {self.iteration}', end='\r')

        current_selection = []

        if self.debug_print:
            debug_print_solution(cnf, solution)

        # Remove tautology
        cnf = self.remove_tautology(cnf)

        # Do unit propogation
        cnf, selected = self.unit_propogation(cnf)
        current_selection = current_selection + selected

        # set pure literals to true
        cnf, _selected = self.set_pure_literal(cnf)

        current_selection = current_selection + _selected

        if self.debug_print:
            self.debug_print_cnf(cnf)

        solution = solution + current_selection
        # check trivial cases
        if [] in cnf:
            self.collate_results(False, solution)
            return False
        if not cnf:
            self.collate_results(True, solution)
            return True

        self.update_stats(cnf)
        # select literal using chosen
        t = self.heuristic(cnf)

        if self.debug_print:
            print('selected literal:', t)

        # update solutions
        negated_branch_solution = list(set(solution + [-t]))

        solution = list(set(solution + [t]))

        # Split on t, try to solve the cnf with t and -t
        branch1, _ = self.reduce(cnf, t)
        branch2, _ = self.reduce(cnf, -t)

        if self.debug_print:
            self.debug_print_branches(branch1, branch2, negated_branch_solution, solution)

        return (self.dpll(branch1, solution=solution) or self.dpll(branch2, solution=negated_branch_solution))

    def debug_print_branches(self, branch1, branch2, negated_branch_solution, solution):
        print('branch')
        print(branch1, '||', branch2)
        print('current solutions')
        print(solution, '||', negated_branch_solution)

    def debug_print_cnf(self, cnf):
        print('unit clauses and pure literals processed. \n')
        print('cnf: \n')
        print(cnf)

    def unit_clause_exists(self, cnf):
        for clause in cnf:
            if len(clause) == 1:
                return True
        return False

    def unit_propogation(self, cnf):
        """
        Set all litreal in unit clauses to true
        Do unit propogation
        """
        selected = []
        while self.unit_clause_exists(cnf):
            t1 = 0

            # check for a unit clause and add to list
            # select literal from unit clause (t1)
            # unit_clauses = []
            _cnf = []
            for clause in cnf[::-1]:
                if len(clause) == 1:
                    t1 = clause[0]
                    break

            # reduce cnf with respect to literal (t1)
            cnf, t1 = self.reduce(cnf, t1)
            selected.append(t1)
            # remove that literal (t1) from literal list
            # if t1 in literal:
            #     literal.remove(t1)

            # return new cnf, literals, literals that were selected
        return (cnf, selected)

    def reduce(self, cnf, t):
        """
        Assumes literal t is true
        does unit propogation after setting t to true
        """
        unit_clauses = []

        # Remove all unit clauses that contain literal t
        _cnf = []
        for clause in cnf:
            if t in clause:
                unit_clauses.append(clause)
            else:
                _cnf.append(clause)

        # Remove literal -t from all clauses
        for clause in cnf:
            if (t * -1) in clause:
                _cnf.remove(clause)
                _cnf.append([x for x in clause if x != -t])

        # if t in literal:
        #         literal.remove(t)

        return _cnf, t

    def is_tautology(self, clause):
        for literal in clause:
            if -literal in clause:
                return (True)
        return (False)

    def remove_tautology(self, cnf):
        for clause in cnf:
            # t = isTautology(clause):
            if self.is_tautology(clause):
                cnf.remove(clause)
        # literal = list(set([item for sublist in cnf for item in sublist] ))
        return (cnf)

    def set_pure_literal(self, cnf):
        literal = list(set([item for sublist in cnf for item in sublist]))
        selection = []

        for t in literal:
            if not -t in literal:
                cnf, selected = self.reduce(cnf, t)
                selection.append(selected)
        # literal = list(set([item for sublist in cnf for item in sublist] ))
        # print(literal == list(set([item for sublist in cnf for item in sublist] )))
        return (cnf, selection)


def dimacs_to_cnf(full_problem):
    clauses = []
    lines = full_problem.split("\n")
    for line in lines:
        if len(line) == 0 or line[0] in ['c', 'p', '%', '0']:
            continue
        clause = [int(x) for x in line.split()[0:-1]]
        clauses.append({x for x in clause})
    return clauses


SUDOKU_RULES_DIMACS = 'sudoku_rules_DIMACS.txt'
SUDOKU_EXAMPLE_DIMACS = 'sudoku_example_DIMACS.txt'


def get_dimacs(sudoku_file_path=SUDOKU_EXAMPLE_DIMACS, rules_path=None):
    print("Resolving SAT " + sudoku_file_path + ":\n")
    sudoku_problem_dimacs = open(sudoku_file_path, 'r').read()
    full_problem = sudoku_problem_dimacs
    if rules_path:
        if rules_path != 'none':
            sudoku_rules_dimacs = open(rules_path, 'r').read()
            full_problem = full_problem + sudoku_rules_dimacs
        elif rules_path == 'none':
            print('No sudoku rules provided')
    return full_problem
