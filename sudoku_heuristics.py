import random
import sys
import itertools


######################################################################################################
# Splitting heuristics:
# DLCS (Dynamic Largest Combined Sum):
#   - Pick v with largest CP(v)+CN(v) (= most frequent v)
#   - If CP(v)>CN(v) then v=1 else v=0
######################################################################################################
# DLIS (Dynamic Largest Individual Sum)
# •Pick v with largest CP(v) or largest CN(v)
# •If CP(v)>CN(v) then v=1 else v=0
######################################################################################################
# Compute for every clause ω and every variable l  (in each phase):
# J(l) := Σ((2)^(-|ω|)) ∀l ∈ ω
# Choose a variable l that maximizes J(l).
# Which means that this strategy gives an exponentially higher weight to literals in shorter clauses.
###
from typing import List, Any


def branching_heuristics_collection(heuristic):
    branching_heuristics = {
        'RANDOM': random_selection,
        'DLCS': dynamic_largest_combined_sum, #AKA: most frequent (unsigned) variable
        'DLIS': dynamic_largest_individual_sum,
        'JEROSLOW_WANG': jeroslow_wang
    }
    try:
        return branching_heuristics[heuristic]
    except:
        sys.exit("ERROR: '{}' Unknown/Unimplemented branching heuristic.".format(heuristic) +
                 "\nImplemented heuristics: {}".format(branching_heuristics.keys()))


def get_literal_occurrence_frequency(cnf_formula):
    merged = list(itertools.chain.from_iterable(cnf_formula))
    x = [item for item in merged]
    return max(set(x), key=x.count)


def get_absolute_literal_occurrence_frequency(cnf_formula):
    merged = list(itertools.chain.from_iterable(cnf_formula))
    x = [abs(item) for item in merged]
    return max(set(x), key=x.count)


def get_weighted_frequency(cnf_formula, weight=2):
    counter = {}
    for clause in cnf_formula:
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


def dynamic_largest_individual_sum(cnf_formula):
    return get_literal_occurrence_frequency(cnf_formula)

def dynamic_largest_combined_sum(cnf_formula):
    return get_absolute_literal_occurrence_frequency(cnf_formula)



def main():
    cnf_formula = [-111, -112], [-111, 122, 123, -112], [-111, 114, -112], [121, 123, -111], [-123, 144, -112], [-111], [144, 112], [112],[112,156,167, 111]

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


    ## Eventually, the heuristic function can be assigned dynamically can be available to the dpll function
    #  by being a class member (via constructor, if we stick to OOP here), or just passed as a parameter directly to the dpll function

if __name__ == '__main__':
    main()