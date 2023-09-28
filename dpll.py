import os
import time
import argparse  # for command line arguments
import numpy as np
import copy
import random

var = set()


def read_input():
    with open('input.cnf', 'r') as file:
        lines = file.read().splitlines()
        output = list()
        output.append(list())  # to handle index out of range error when accessing last sublist [-1]
        for line in lines:
            vals = line.split(' ')
            if vals[0] != "p" and vals[0] != "c" and len(vals) != 0:
                for val in vals:
                    var.add(abs(int(val)))
                    if val == '0':  # signifies end of clause
                        output.append(list())
                    else:
                        output[-1].append(int(val))  # add to current list
        if len(output[-1]) == 0:
            output.pop()
        num_var = len(var) - 1
        var.clear()
        return output, num_var


def dpll_random(clause, assignments, i):
    i += 1
    unit_clause(clause, assignments)  # generate assignments

    if len(clause) == 0:  # nothing left to assign
        return True, assignments, i
    elif len(min(clause, key=len)) == 0:
        return False, assignments, i

    # split and look into subcases
    left = list(var - set(np.absolute(assignments)))  # take out variables from 1-125
    prop = random.choice(left)  # random heuristic

    temp_vals = copy.deepcopy(assignments)
    temp_clause = copy.deepcopy(clause)
    temp_clause.append([-prop])

    truth_val, temp_vals, pointer = dpll_random(temp_clause, temp_vals, i)
    if truth_val:
        return True, temp_vals, pointer

    # repeat with negation, checking all possibilities --> splitting rule
    temp_vals = copy.deepcopy(assignments)
    temp_clause = copy.deepcopy(clause)
    temp_clause.append([prop])

    return dpll_random(temp_clause, temp_vals, i)


def unit_clause(clause, vals):
    while len(min(clause, key=len)) == 1:  # while there is a unit clause
        unit = min(clause, key=len)
        if -unit[0] in vals:  # if invalid assignment
            clause.append([])
        elif not unit[0] in vals:  # add to assignment
            vals.append(unit[0])
        clause.remove(unit) # since we have dealt with this unit clause, remove from list
        if len(clause) == 0:
            return

    # remove all occurrences in other clauses
    for val in vals:
        for c in clause[:]:
            if val in c:
                clause.remove(c)
            if (-1 * val) in c:
                c.remove(-1 * val)


def solution(truth, assignments, clause, num_of_var, elapsed, i):
    vals = [("v " + str(x)) for x in assignments]
    sol_time = os.linesep.join(["t cnf" + (" 1 " if truth else " 0 ") + str(num_of_var) + " " + str(clause) + " " + str(elapsed) + " " + str(i), os.linesep.join(vals)])
    sol_final = os.linesep.join(["c Solution to Puzzle", os.linesep.join(["s cnf" + (" 1 " if truth else " 0 ") + str(num_of_var) + " " + str(clause), sol_time])])

    return sol_final


if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument("--heuristic", help="the heuristic to run (random, two-clause)")
    args = argParser.parse_args()

    random.seed(510260)
    vals = list()
    cnf, var_num = read_input()
    clauses = len(cnf)
    var = set(range(1, var_num + 1))
    i = 0

    start = time.time()
    # after other implementations, can access heuristic type using args.heuristic
    boolean, final_vals, i = dpll_random(cnf, vals, i)  # recursively call it
    end = time.time()
    total_time = end - start
    final_vals.sort()

    with open('output.cnf', 'w') as file:
        final = solution(boolean, final_vals, clauses, var_num, total_time, i)
        file.write(final)

