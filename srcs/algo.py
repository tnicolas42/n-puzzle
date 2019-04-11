#!/usr/bin/python3
import copy
import srcs.global_var as g
from srcs.stats import get_stats
from srcs.heuristics import heuristic_list
from heapq import heapify, heappush, heappop, nsmallest


def get_all_childs(puzzle, heuristic, auto_update=True):
    """
    get all childs from a puzzle
    """
    childs = []

    # create child only with specifics confitions
    if puzzle.last_move is not 'B' and puzzle.pos0xy[0] > 0:
        childs.append(copy.deepcopy(puzzle).move('T', auto_update=auto_update))
    if puzzle.last_move is not 'T' and puzzle.pos0xy[0] < puzzle.size - 1:
        childs.append(copy.deepcopy(puzzle).move('B', auto_update=auto_update))
    if puzzle.last_move is not 'R' and puzzle.pos0xy[1] > 0:
        childs.append(copy.deepcopy(puzzle).move('L', auto_update=auto_update))
    if puzzle.last_move is not 'L' and puzzle.pos0xy[1] < puzzle.size - 1:
        childs.append(copy.deepcopy(puzzle).move('R', auto_update=auto_update))

    for i in range(len(childs) - 1, -1, -1):
        childs[i].init_child(parent=puzzle, _heuristic=heuristic)
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
        childs = get_all_childs(lastUsed, heuristic=heuristic, auto_update=auto_update_heuristic)

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

            if child_open_cpy is not None and opened[child_open_cpy] >= child:
                opened[child_open_cpy] = child
                heapify(opened) # heapify because we have changed element value

            if child_close_cpy is not None and closed[child.hash] >= child:
                closed[child.hash] = child

    return None  # the resolution is impossible
