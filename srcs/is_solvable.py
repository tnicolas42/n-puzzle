from srcs.generate_puzzle import generate_puzzle, spiral
from srcs.stats import get_stats


def inversions(start):
    """
    An inversion is when a tile precedes another tile with a lower number on it
    The solution state has zero inversions
    """
    _spiral = spiral(start.size, start)

    inversions = 0
    for i, val in enumerate(_spiral):
        if val != 0:
            for next in _spiral[i + 1:]:
                inversions += 1 if (next < val and next != 0) else 0
    return inversions

@get_stats
def is_solvable(start):
    """
    Definition: the polarity of a number is whether the number is even or odd.

    Returns true if `start` belongs to the same permutation group as `goal`
    Anny permutation result to the same polarity.
    because anny permtation add -2 or +0 or +2 inversions
    """
    start_inversions = inversions(start)
    goal_inversions = 0

    return int(start_inversions % 2) == int(goal_inversions % 2)
