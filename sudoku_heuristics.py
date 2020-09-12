import random
import sys


# Branching heuristics
from typing import List, Tuple


def branching_heuristics_collection(heuristic):
    branching_heuristics = {
        'RANDOM': random_selection,
        'MOST_FREQUENT': most_frequent,
        'JW': jeroslow_wang
    }
    try:
        return branching_heuristics[heuristic]
    except:
        sys.exit("ERROR: '{}' Unknown/Unimplemented branching heuristic.".format(heuristic) +
                 "\nImplemented heuristics: {}".format(branching_heuristics.keys()))


def get_literal_occurrence_frequency(cnf_formula):
    counter = {}
    for clause in cnf_formula:
        for literal in clause:
            if literal in counter:
                counter[literal] += 1
            else:
                counter[literal] = 1
    return counter


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

def jeroslow_wang(cnf_formula):
    counter = get_weighted_frequency(cnf_formula)
    return max(counter, key=counter.get)

def most_frequent(cnf_formula):
    counter = get_literal_occurrence_frequency(cnf_formula)
    return max(counter, key=counter.get)


def main():
    cnf_formula = [111, -112], [111, 122, 123], [-111, 114], [121, 123], [-123, 144], [111], [144]

    random_heuristic = branching_heuristics_collection("RANDOM")
    lucky_literal = random_heuristic(cnf_formula)
    print("The lucky literal is ", lucky_literal)

    most_frequent_heuristic = branching_heuristics_collection("MOST_FREQUENT")
    most_frequent = most_frequent_heuristic(cnf_formula)
    print("The most frequent literal is ", most_frequent)

    ## Eventually, the heuristic function can be assigned dynamically can be available to the dpll function
    #  by being a class member (via constructor, if we stick to OOP here), or just passed as a parameter directly to the dpll function

if __name__ == '__main__':
    main()