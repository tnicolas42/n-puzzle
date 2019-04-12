#!/usr/bin/python3
import sys
import random
import argparse
import traceback
import srcs.global_var as g
from srcs.generate_puzzle import generate_puzzle, generate_random
from srcs.parser import parse_from_file, parse
from srcs.is_solvable import is_solvable
from srcs.stats import print_stats, EnableStats
from srcs.algo import a_star_algo, heuristic_list


admissible_heuristics = ('manhattan', 'hamming', 'linear_conflict')

param = dict(
    heuristic='linear_conflict',
    auto_update_heuristic=True,
    greedy_search=False,
    super_fast=False,
    resolved_puzzle=None,
    size=None,  # 3 if 3*3
    total_size=None,  # 9 if 3*3
)

BOLD = "\033[1m"
EOC = "\x1B[0m"

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("puzzle", type=str, default="", nargs='?',
                            help="The file that contain the puzzle")
        parser.add_argument("--heuristic", type=str, default=param['heuristic'], choices=admissible_heuristics,
                            help="This is the heuristic function")
        parser.add_argument("-s", "--stats", action="store_true", default=False,
                            help="Print stats about functions [for debug]")
        parser.add_argument("--silent", action="store_true", default=False,
                            help="Don't display all the puzzles states on the output")
        parser.add_argument("--disable-auto-update", action="store_false", default=True,
                            help="Disable the auto update of heuristic")

        parser.add_argument("-r", "--random", type=int, default=-1,
                            help="Generate a random puzzle of a given size")
        parser.add_argument("--generate-solvable", action="store_true", default=False,
                            help="Generate only solvable puzzle")
        parser.add_argument("--generate-unsolvable", action="store_true", default=False,
                            help="Generate only unsolvable puzzle")

        parser.add_argument("-u", "--uniform-cost", action="store_true", default=False,
                            help="Set an uniform cost (heuristic funcion return 0) -> it's like dijkstra")
        parser.add_argument("-g", "--greedy", action="store_true", default=False,
                            help="Go to only one path, used to find a solution very quickly but it's not the better path")
        parser.add_argument("-f", "--super-fast", action="store_true", default=False,
                            help="Super fast algoritm -> just ignore the distance from start")

        args = parser.parse_args()

        EnableStats.enable = args.stats
        param['auto_update_heuristic'] = args.disable_auto_update
        param['greedy_search'] = args.greedy
        param['super_fast'] = args.super_fast
        # select the right heuristic function
        param['heuristic'] = args.heuristic
        if args.uniform_cost:
            param['heuristic'] = 'uniform_cost'

        # init the global vairable
        g.init_global(param_=param)

        if args.random > 0:
            # init some params about size
            g.param['size'] = args.random
            g.param['total_size'] = args.random * args.random
        elif args.puzzle == "":
            data = "".join(sys.stdin.readlines())
            puzzle = parse(data)
            if puzzle is None:
                exit(1)
        else:
            puzzle = parse_from_file(sys.argv[1])
            if puzzle is None:
                exit(1)

        # create a resolved puzzle
        param['resolved_puzzle'] = generate_puzzle(param['size'])

        if args.random > 0:
            # generate a random puzzle
            if args.generate_solvable:
                puzzle = generate_random(solvable=True)
            elif args.generate_unsolvable:
                puzzle = generate_random(solvable=False)
            else:
                puzzle = generate_random(solvable=random.choice([True, False]))

        # if the puzzle is not solvable
        if not is_solvable(puzzle):
            print("this npuzzle is unsolvable")
            print(puzzle)
            exit(1)


        # get the heuristic for the first puzzle
        puzzle.calc_heuristic()
        # start the main algo
        result = a_star_algo(puzzle)

        if not result and param['greedy_search']:
            param['greedy_search'] = False
            print('unable to get the solution with a greedy algoritm, retry without greedy')
            result = a_star_algo(puzzle)

        # if the algo fail (no solution)
        if not result:
            print("after trying to resolve it, this npuzzle is unsolvable")
            print(puzzle)
            exit(1)

        # prin the result
        print("base puzzle:")
        print(puzzle)
        if args.silent:
            print("result:")
            print(result['puzzle'])
        else:
            list_puzzle = result['puzzle'].get_all_puzzles()
            for i in range(1, len(list_puzzle)):
                print(BOLD + 'move %d: -> %s%s' % (i, list_puzzle[i].last_move,
                    (' [solved puzzle]' if i+1 == len(list_puzzle) else "") + EOC))
                print(list_puzzle[i])
        path = result['puzzle'].get_path()
        if param['greedy_search']:
            print('using greedy algoritm')
        if param['super_fast']:
            print('using super fast algo')
        print('all moves (%s%d%s): %s' % (BOLD, len(path), EOC, path))
        print('max opened at the same time: %s%d%s' % (BOLD, result['max_opened'], EOC))
        print('total opened: %s%d%s -> using %s' % (BOLD, result['total_opened'], EOC, param['heuristic']))
    except Exception as e:
        traceback.print_exc()

    print_stats()
