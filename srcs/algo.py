import copy
import srcs.global_var as g


def heuristic_manhattan(puzzle):
    total = 0
    for i in range(g.total_size):
        total += puzzle.get_dist_from_goal(i)
    return total


def get_dist_form_start(puzzle):
    return puzzle.dist_from_start


def get_total_dist(puzzle, heuristic_func):
    """
    get dist from start + heuristic
    """
    return get_dist_form_start(puzzle) + heuristic_func(puzzle)


def get_min_puzzle_index(opened, heuristic_func):
    """
    get the "best" puzzle from opened list
    """
    min_index = 0
    min_dist = get_total_dist(opened[0], heuristic_func)

    for i in range(1, len(opened)):
        dist = get_total_dist(opened[i], heuristic_func)
        if dist < min_dist:
            min_dist = dist
            min_index = i

    return min_index


def get_all_childs(puzzle):
    """
    get all childs from a puzzle
    """
    childs = [
        copy.deepcopy(puzzle).move('T'),
        copy.deepcopy(puzzle).move('B'),
        copy.deepcopy(puzzle).move('L'),
        copy.deepcopy(puzzle).move('R'),
    ]
    for i in range(len(childs) - 1, -1, -1):
        if puzzle == childs[i]:
            childs.pop(i)
        else:
            # add a link to the parent
            childs[i].set_parent(puzzle)
    return childs



def a_star_algo(puzzle, heuristic_func=heuristic_manhattan):
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
        used = get_min_puzzle_index(opened, heuristic_func)
        # put this node in closed
        closed.append(opened[used])
        opened.pop(used)
        # get all childs of the selected path
        childs = get_all_childs(closed[-1])
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

            if child_open_cpy == None and child_close_cpy == None:
                opened.append(child)
                result['total_opened'] += 1
            if child_open_cpy is not None and get_total_dist(opened[child_open_cpy], heuristic_func) > get_total_dist(child, heuristic_func):
                opened[child_open_cpy] = child
            if child_close_cpy is not None and get_total_dist(closed[child_close_cpy], heuristic_func) > get_total_dist(child, heuristic_func):
                closed[child_close_cpy] = child
    return None  # the resolution is impossible