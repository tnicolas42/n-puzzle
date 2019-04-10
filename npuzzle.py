#!/usr/bin/python3
import sys
import argparse
import srcs.global_var as g
from srcs.generate_puzzle import generate_puzzle
from srcs.parser import parse_from_file, parse
from srcs.is_solvable import is_solvable
from srcs.stats import print_stats, EnableStats
from srcs.algo import a_star_algo

admissible_heuristics = ('manhattan', 'hamming')

param = dict(
    heuristic='manhattan',
    auto_update_heuristic=True,
)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("puzzle", type=str, default="", nargs='?',
                        help="The file that contain the puzzle")
    parser.add_argument("--heuristic", type=str, default="manhattan", choices=admissible_heuristics,
                        help="This is the heuristic function")
    parser.add_argument("--stats", action="store_true", default=False,
                        help="Print stats about functions [for debug]")
    args = parser.parse_args()

    EnableStats.enable = args.stats

    if args.puzzle == "":
        data = "".join(sys.stdin.readlines())
        puzzle = parse(data)
        if puzzle is None:
            exit(1)
    else:
        puzzle = parse_from_file(sys.argv[1])
        if puzzle is None:
            exit(1)

    if not is_solvable(puzzle):
        print("this npuzzle is unsolvable")
        print(puzzle)
        exit(1)

    resolv_puzzle = generate_puzzle(puzzle.size)
    total_sz = puzzle.size * puzzle.size
    g.init_global(puzzle=resolv_puzzle, total_size_=total_sz)  # generate the resolved puzzle

    result = a_star_algo(puzzle, **param)

    print(puzzle)
    print(result['puzzle'].get_path())
    print(result['puzzle'])
    print('max opened at the same time: %d' % (result['max_opened']))
    print('total opened: %d' % (result['total_opened']))
    print_stats()
