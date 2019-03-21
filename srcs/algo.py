import srcs.global_var as g


def heuristic_manhattan(puzzle):
    total = 0
    for i in range(g.total_size):
        total += puzzle.get_dist_from_goal(i)
    return total

def a_star_algo(puzzle, heuristic_func=heuristic_manhattan):
    dist_to_goal = heuristic_func(puzzle)
    print(puzzle)
    print("dist to goal -> %d" % (dist_to_goal))
