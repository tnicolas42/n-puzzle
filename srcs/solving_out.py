from srcs.algo import a_star_algo, heuristic_list
import srcs.global_var as g

BOLD = "\033[1m"
EOC = "\x1B[0m"

def solving_out(puzzle):
    # get the heuristic for the first puzzle
    puzzle.calc_heuristic()
    # start the main algo
    result = a_star_algo(puzzle)

    if not result and g.param['greedy_search']:
        g.param['greedy_search'] = False
        print('unable to get the solution with a greedy algoritm, retry without greedy')
        result = a_star_algo(puzzle)

    # if the algo fail (no solution)
    if not result:
        print("after trying to resolve it, this npuzzle is unsolvable")
        print(puzzle)
        exit(1)

    # print the result
    print("base puzzle:")
    print(puzzle)
    if g.args.silent:
        print("result:")
        print(result['puzzle'])
    else:
        list_puzzle = result['puzzle'].get_all_puzzles()
        for i in range(1, len(list_puzzle)):
            print(BOLD + 'move %d: -> %s%s' % (i, list_puzzle[i].last_move,
                (' [solved puzzle]' if i+1 == len(list_puzzle) else "") + EOC))
            print(list_puzzle[i])
    path = result['puzzle'].get_path()
    if g.param['greedy_search']:
        print('using greedy algoritm')
    if g.param['super_fast']:
        print('using super fast algo')
    print('all moves (%s%d%s): %s' % (BOLD, len(path), EOC, path))
    print('max opened at the same time: %s%d%s' % (BOLD, result['max_opened'], EOC))
    print('total opened: %s%d%s -> using %s' % (BOLD, result['total_opened'], EOC, g.param['heuristic']))

    return result