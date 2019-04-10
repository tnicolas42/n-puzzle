#!/usr/bin/python3
import copy
import srcs.global_var as g
from srcs.stats import get_stats
from heapq import heapify, heappush, heappop, nsmallest

def heuristic_manhattan(puzzle):
    if puzzle.dist_to_goal is not None:  # if the distance are already calculated
        return puzzle.dist_to_goal
    total = 0
    for i in range(g.total_size):
        total += puzzle.get_dist_from_goal(i)
    puzzle.dist_to_goal = total
    return total


heuristic_list = dict(  # list of all heuristic function
    manhattan=heuristic_manhattan,
)

@get_stats
def get_total_dist(puzzle, heuristic):
    """
    get dist from start + heuristic
    """
    return puzzle.dist_from_start + puzzle.dist_to_goal


def get_all_childs(puzzle, heuristic):
    """
    get all childs from a puzzle
    """
    childs = []

    # create child only with specifics confitions
    if puzzle.last_move is not 'B' and puzzle.pos0xy[0] > 0:
        childs.append(copy.deepcopy(puzzle).move('T', heuristic=heuristic))
    if puzzle.last_move is not 'T' and puzzle.pos0xy[0] < puzzle.size - 1:
        childs.append(copy.deepcopy(puzzle).move('B', heuristic=heuristic))
    if puzzle.last_move is not 'R' and puzzle.pos0xy[1] > 0:
        childs.append(copy.deepcopy(puzzle).move('L', heuristic=heuristic))
    if puzzle.last_move is not 'L' and puzzle.pos0xy[1] < puzzle.size - 1:
        childs.append(copy.deepcopy(puzzle).move('R', heuristic=heuristic))

    for i in range(len(childs) - 1, -1, -1):
        childs[i].init_child(parent=puzzle)
    return childs


@get_stats
def a_star_algo(puzzle, heuristic='manhattan', auto_update_heuristic=True):
    """
    it is the main function to solv the n-puzzle

    return a dict
    dict(
        max_opened -> max puzzle opened at the same time
        total_opened -> total puzzle opened
        puzzle -> the last puzzle
    )
    """
    opened = []
    heappush(opened, puzzle)
    closed = dict()

    result = dict(
        max_opened=0,
        total_opened=1,
        puzzle=None,
    )

    while opened != []:
        result['max_opened'] = max(result['max_opened'], len(opened))

        # get the puzzle with the min dist from start in opened
        used = heappop(opened)
        # put this node in closed
        closed[used.hash] = used
        lastUsed = used
        # get all childs of the selected path
        if auto_update_heuristic:
            childs = get_all_childs(lastUsed, heuristic=heuristic)
        else:
            childs = get_all_childs(lastUsed, heuristic=None)

        for child in childs:

            # check if it is finish
            if child == g.resolved_puzzle:
                result['puzzle'] = child
                return result  # the algo is finished

            # look for child in opened or closed
            child_open_cpy = None  # index of a copy of child in opened (if exist)
            try:
                child_open_cpy = opened.index(child)
            except ValueError:
                pass
            child_close_cpy = None  # index of a copy of child in closed (if exist)
            if child_open_cpy is None:
                if child.hash in closed:
                    child_close_cpy = child

            if child_open_cpy is None and child_close_cpy is None:
                heappush(opened, child)
                result['total_opened'] += 1

            if child_open_cpy is not None and \
               get_total_dist(opened[child_open_cpy], heuristic) > get_total_dist(child, heuristic):
                opened[child_open_cpy] = child
                heapify(opened) # heapify because we have changed element value

            if child_close_cpy is not None and \
               get_total_dist(closed[child.hash], heuristic) > get_total_dist(child, heuristic):
                closed[child.hash] = child

    return None  # the resolution is impossible
