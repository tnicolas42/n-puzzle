#!/usr/bin/python3
import srcs.global_var as g

def heuristic_manhattan(puzzle):
    """
    return the sum of all dist btw puzzles and goals
    """
    if puzzle.dist_manhattan is not None:  # if the distance are already calculated
        return puzzle.dist_manhattan
    total = 0
    for i in range(g.total_size):
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
    for i in range(g.total_size):
        total += not puzzle.is_well_placed(i)
    puzzle.dist_to_goal = total
    return total


def heuristic_linear_conflict(puzzle):
    """
    reuturn the manhattan distance + the number of linear conflicts * 2
    """
    inversions = 0
    for x1 in range(puzzle.size):
        for y1 in range(puzzle.size):
            if puzzle.get(x1, y1) != 0:
                pos_col = puzzle.is_in_column(x1, y1)
                if pos_col:
                    list_upper = []  # list of all elements upper
                    for x2 in range(pos_col[0]):
                        list_upper.append(g.resolved_puzzle.get(x2, y1))
                    for x2 in range(x1+1, puzzle.size):
                        if puzzle.get(x2, y1) != 0:
                            if puzzle.get(x2, y1) in list_upper:
                                inversions += 1

                pos_ln = puzzle.is_in_line(x1, y1)
                if pos_ln:
                    list_upper = []  # list of all elements upper
                    for y2 in range(pos_ln[1]):
                        list_upper.append(g.resolved_puzzle.get(x1, y2))
                    for y2 in range(y1+1, puzzle.size):
                        if puzzle.get(x1, y2) != 0:
                            if puzzle.get(x1, y2) in list_upper:
                                inversions += 1

    puzzle.dist_to_goal = heuristic_manhattan(puzzle) + inversions * 2
    return puzzle.dist_to_goal


heuristic_list = dict(  # list of all heuristic function
    manhattan=heuristic_manhattan,
    hamming=heuristic_hamming,
    linear_conflict=heuristic_linear_conflict,
)