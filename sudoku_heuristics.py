import random
import sys
import itertools


######################################################################################################
###                        Splitting heuristics:
###
###        DLCS (Dynamic Largest Combined Sum):
#    • Pick v with largest CP(v)+CN(v) (= most frequent v)
#    • If CP(v)>CN(v) then v=1 else v=0
######################################################################################################
###        DLIS (Dynamic Largest Individual Sum)
#
#     • Pick v with largest CP(v) or largest CN(v)
#     • If CP(v)>CN(v) then v=1 else v=0
###
######################################################################################################
###
###        JEROSLOW_WANG
# Compute for every clause ω and every variable l  (in each phase):
# J(l) := Σ((2)^(-|ω|)) ∀l ∈ ω
# Choose a variable l that maximizes J(l).
# Which means that this strategy gives an exponentially higher weight to literals in shorter clauses.
###
######################################################################################################
###
###        MOM Maximum number of Occurrences in the Minimum length clauses.
###
###  Prefers literal having Maximum number of Occurrences in the Minimum length clauses.
#    This means that the clauses having minimal length are considered, as more meaningful
######################################################################################################

def branching_heuristics_collection(heuristic):

    try:
        return branching_heuristics[heuristic]
    except:
        sys.exit("ERROR: '{}' Unknown/Unimplemented branching heuristic.".format(heuristic) +
                 "\nImplemented heuristics: {}".format(branching_heuristics.keys()))

def getMostCommonLiteralNegative(cnf):
        """
        Finds and returns the negative of literal that occurs the most in cnf
        """
        merged = list(itertools.chain(*cnf))    
        
        return max(set(merged), key=merged.count)*-1
         

def get_literal_occurrence_frequency(cnf_formula):
    merged = list(itertools.chain.from_iterable(cnf_formula))
    x = [item for item in merged]
    return max(set(x), key=x.count)


def get_absolute_literal_occurrence_frequency(cnf_formula):
    merged = list(itertools.chain.from_iterable(cnf_formula))
    x = [abs(item) for item in merged]
    return max(set(x), key=x.count)


def get_weighted_frequency(cnf_formula, weight=2, is_absolute=False):
    counter = {}
    for clause in cnf_formula:
        if (is_absolute): literal = abs(literal)
        for literal in clause:
            if literal in counter:
                counter[literal] += weight ** -len(clause)
            else:
                counter[literal] = weight ** -len(clause)
    return counter

def random_selection(cnf_formula):
    return random.choice(unique_literals(cnf_formula))

def unique_literals(cnf_formula: list()):
    unique_values = list(set(x for l in cnf_formula for x in l))
    return unique_values

###
# Compute for every clause ω and every variable l  (in each phase):
# J(l) := Σ((2)^(-|ω|)) ∀l ∈ ω
# Choose a variable l that maximizes J(l).
# Which means that this strategy gives an exponentially higher weight to literals in shorter clauses.
###
def jeroslow_wang(cnf_formula):
    counter = get_weighted_frequency(cnf_formula)
    return max(counter, key=counter.get)

def jeroslow_wang_two_sided(formula):
    counter = get_weighted_frequency(formula, True)
    return max(counter, key=counter.get)

def dynamic_largest_individual_sum(cnf_formula):
    return get_literal_occurrence_frequency(cnf_formula)

def dynamic_largest_combined_sum(cnf_formula):
    return get_absolute_literal_occurrence_frequency(cnf_formula)

def get_difference_counter(formula):
    counter = {}
    for clause in formula:
        for literal in clause:
            if literal in counter:
                if literal > 0:
                    counter[literal] += 1
                else:
                    counter[-literal] += - 1
            else:
                if literal > 0:
                    counter[literal] = 1
                else:
                    counter[-literal] = - 1
    return counter


branching_heuristics = {
        'RANDOM': random_selection,
        'DLCS': dynamic_largest_combined_sum, #AKA: most frequent (unsigned) variable
        'DLIS': dynamic_largest_individual_sum,
        'JEROSLOW_WANG': jeroslow_wang,
        'JEROSLOW_WANG_TWO_SIDED': jeroslow_wang_two_sided,
        'most_common_negative':getMostCommonLiteralNegative
    }
heuristic_list = list(branching_heuristics.keys())

def main():
    cnf_formula = [-111, -112], [-111, 122, 123, -112], [-111, 114, -112], [121, 123, -111], [-123, 144, -112], [-111, 198], [144, 112], [112],[112,156,167, 111], [555], [555]

    random_heuristic = branching_heuristics_collection("RANDOM")
    lucky_literal = random_heuristic(cnf_formula)
    print("The lucky literal is ", lucky_literal)

    most_frequent_heuristic = branching_heuristics_collection("DLCS")
    most_frequent_combined = most_frequent_heuristic(cnf_formula)
    print("The most frequent combined sum literal is ", most_frequent_combined)
    assert most_frequent_combined==112, "Most DLCS frequent (combined sum) literal is -112"

    most_frequent_heuristic = branching_heuristics_collection("DLIS")
    most_frequent_individual = most_frequent_heuristic(cnf_formula)
    assert most_frequent_individual==-111, "Most DLIS frequent (individual sum) literal is 111"
    print("The most frequent individual sum literal is ", most_frequent_individual)

    most_frequent_heuristic = branching_heuristics_collection("JEROSLOW_WANG")
    most_frequent_jw = most_frequent_heuristic(cnf_formula)
    assert most_frequent_jw==555, "Most JEROSLOW_WANG frequent literal is 555"
    print("The most frequent individual sum literal is ", most_frequent_jw)

    # Eventually, the heuristic function can be assigned dynamically can be available to the dpll function
    # by being a class member (via constructor, if we stick to OOP here), or just passed as a parameter directly to the dpll function

if __name__ == '__main__':
    main()