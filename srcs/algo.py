import copy
import srcs.global_var as g
from srcs.stats import get_stats


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


def get_dist_form_start(puzzle):
    return puzzle.dist_from_start


@get_stats
def get_total_dist(puzzle, heuristic):
    """
    get dist from start + heuristic
    """
    return get_dist_form_start(puzzle) + heuristic_list[heuristic](puzzle)


@get_stats
def get_min_puzzle_index(opened, heuristic):
    """
    get the "best" puzzle from opened list
    """
    min_index = 0
    min_dist = get_total_dist(opened[0], heuristic)

    for i in range(1, len(opened)):
        dist = get_total_dist(opened[i], heuristic)
        if dist < min_dist:
            min_dist = dist
            min_index = i

    return min_index


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
    opened = [puzzle]
    closed = []

    result = dict(
        max_opened=0,
        total_opened=1,
        puzzle=None,
    )

    while opened != []:
        result['max_opened'] = max(result['max_opened'], len(opened))

        # get the puzzle with the min dist from start in opened
        used = get_min_puzzle_index(opened, heuristic)
        # put this node in closed
        closed.append(opened[used])
        opened.pop(used)
        # get all childs of the selected path
        if auto_update_heuristic:
            childs = get_all_childs(closed[-1], heuristic=heuristic)
        else:
            childs = get_all_childs(closed[-1], heuristic=None)

        for child in childs:

            # check if it is finish
            if child == g.resolved_puzzle:
                result['puzzle'] = child
                return result  # the algo is finished

            # look for child in opened or closed
            child_open_cpy = None  # index of a copy of child in opened (if exist)
            for i in range(len(opened)):
                if opened[i] == child:
                    child_open_cpy = i
                    break
            child_close_cpy = None  # index of a copy of child in closed (if exist)
            for i in range(len(closed)):
                if closed[i] == child:
                    child_close_cpy = i
                    break

            if child_open_cpy is None and child_close_cpy is None:
                opened.append(child)
                result['total_opened'] += 1

            if child_open_cpy is not None and \
               get_total_dist(opened[child_open_cpy], heuristic) > get_total_dist(child, heuristic):
                opened[child_open_cpy] = child

            if child_close_cpy is not None and \
               get_total_dist(closed[child_close_cpy], heuristic) > get_total_dist(child, heuristic):
                closed[child_close_cpy] = child

    return None  # the resolution is impossible
