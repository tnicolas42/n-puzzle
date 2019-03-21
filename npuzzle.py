import sys
import srcs.global_var as g
from srcs.generate_puzzle import generate_puzzle
from srcs.parser import parse_from_file, parse
from srcs.algo import a_star_algo


if __name__ == "__main__":
    if len(sys.argv) == 2:
        puzzle = parse_from_file(sys.argv[1])
        if puzzle is None:
            exit(1)
    elif len(sys.argv) > 2:
        print("usage:\n"
              "python3 npuzzle.py <file>"
              "cat <file> | python3 npuzzle.py")
        exit(1)
    else:
        data = "".join(sys.stdin.readlines())
        puzzle = parse(data)
        if puzzle is None:
            exit(1)

    resolv_puzzle = generate_puzzle(puzzle.size)
    total_sz = puzzle.size * puzzle.size
    g.init_global(puzzle=resolv_puzzle, total_size_=total_sz)  # generate the resolved puzzle

    print(puzzle)
    result = a_star_algo(puzzle)
    print(result.get_path())
    print(result)

