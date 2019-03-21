from srcs.puzzle import Puzzle


def parse(npuzzle_str):
    size_puzzle = None
    puzzle = []

    npuzzle = npuzzle_str.split('\n')

    for full_line in npuzzle:
        line = full_line.strip()  # remove spaces
        if line == "" or line[0] == '#':  # ignore comment
            continue
        line = line.split('#')[0].strip()  # remove comment at the end of a line

        if size_puzzle is None:
            try:
                size_puzzle = int(line)
            except ValueError:
                print("[ERROR]: invalid line: '%s'" % (full_line))
                return None

        else:
            all_val = line.split()
            for i in range(len(all_val)):
                try:
                    all_val[i] = int(all_val[i])
                except ValueError:
                    print("[ERROR]: invalid line: '%s'" % (full_line))
                    return None
            if len(all_val) == size_puzzle:
                puzzle.extend(all_val)
            else:
                print('[ERROR]: line must be of size %d not %d -> %s' % (size_puzzle, len(all_val), full_line))
                return None

    if size_puzzle is None:
        print('[ERROR]: invalid file')
        return None
    if len(puzzle) != size_puzzle * size_puzzle:
        print('[ERROR]: invalid puzzle size')
        return None

    # check number (from 0 to size * size - 1)
    all_count = [0 for i in range(size_puzzle * size_puzzle)]
    for nb in puzzle:
        if nb >= size_puzzle * size_puzzle or nb < 0:
            print("[ERROR]: invalid value: %d" % (nb))
            return None
        all_count[nb] += 1
    for i in range(len(all_count)):
        if all_count[i] > 1:
            print("[ERROR]: cannot have multiple same values %d" % (i))
            return None
        elif all_count[i] == 0:
            print('[ERROR]: value %d is missing' % (i))
            return None

    return Puzzle(size=size_puzzle, puzzle=puzzle)


def parse_from_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    return parse(content)
