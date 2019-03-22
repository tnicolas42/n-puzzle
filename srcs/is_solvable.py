from srcs.generate_puzzle import generate_puzzle, spiral
from srcs.stats import get_stats


def inversions(start, goal=None):
    """
    An inversion is when a tile precedes another tile with a lower number on it
    The solution state has zero inversions
    """
    if goal is None:
        goal = generate_puzzle(start.size)

    _spiral = spiral(start.size, start)

    inversions = 0
    for i, val in enumerate(_spiral):
        if val != 0:
            for next in _spiral[i + 1:]:
                inversions += 1 if (next < val and next != 0) else 0
    return inversions


@get_stats
def is_solvable(start, goal=None):
    """
    Returns true if `start` belongs to the same permutation group as `goal`
    """
    if goal is None:
        goal = generate_puzzle(start.size)

    start_inversions = inversions(start, goal)
    goal_inversions = 0

    # In this case, the row of the '0' tile matters
    if start.size % 2 == 0:
        start_inversions += start.index(0) / start.size
        goal_inversions += goal.index(0) / start.size

    return int(start_inversions % 2) == int(goal_inversions % 2)
