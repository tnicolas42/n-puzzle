#!/usr/bin/python3
import srcs.global_var as g
from srcs.stats import get_stats


def heuristic_manhattan(puzzle):
    """
    return the sum of all dist btw puzzles and goals
    """
    if puzzle.dist_manhattan is not None:  # if the distance are already calculated
        return puzzle.dist_manhattan
    total = 0
    for i in range(g.param['total_size']):
        total += puzzle.get_dist_from_goal(i)
    puzzle.dist_manhattan = total
    puzzle.dist_to_goal = total
    return total


def heuristic_hamming(puzzle):
    """
    return the number of misplaced puzzle
    """
    if puzzle.dist_to_goal is not None:  # if the distance are already calculated
        return puzzle.dist_to_goal
    total = 0
    for i in range(g.param['total_size']):
        total += not puzzle.is_well_placed(i)
    puzzle.dist_to_goal = total
    return total

def heuristic_linear_conflict(puzzle):
    """
    reuturn the manhattan distance + the number of linear conflicts * 2
    """
    if puzzle.dist_manhattan is not None and puzzle.dist_to_goal is not None:
        return puzzle.dist_to_goal
    inversions = 0
    for x1 in range(g.param['size']):
        for y1 in range(g.param['size']):
            inversions += puzzle.get_inversions(x1, y1)
    puzzle.dist_to_goal = heuristic_manhattan(puzzle) + inversions * 2
    return puzzle.dist_to_goal

def heuristic_uniform_cost(puzzle):
    """
    always return the same cost
    this is to run the dijkstra algoritm
    """
    return 0


heuristic_list = dict(  # list of all heuristic function
    manhattan=heuristic_manhattan,
    hamming=heuristic_hamming,
    linear_conflict=heuristic_linear_conflict,
    uniform_cost=heuristic_uniform_cost,
)