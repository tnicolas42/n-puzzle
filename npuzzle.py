import sys
from srcs.parser import parse_from_file, parse

"""
puzzle format:
    for 3*3 puzzle
    [1, 2, 3, 8, 0, 4, 7, 6, 5]
"""

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

    print(list(puzzle))
    print(puzzle)
