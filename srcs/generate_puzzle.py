from puzzle import Puzzle

def generate_puzzle(size, puzzle=None, start_pos=None, start_nb=None):
    """
    Generate a valid puzzle of given size
    """
    if puzzle is None:
        puzzle = [0 for i in range(size*size)]
    if start_pos is None:
        start_pos = [0, 0]
    if start_nb is None:
        start_nb = 1
    
    puzzle = Puzzle(size, puzzle)
    nb = start_nb

    for i in range(size - 2 * start_pos[0]):
        puzzle.set(start_pos[0], start_pos[1] + i, nb)
        nb += 1
    
    for i in range(size - 2 * start_pos[1] - 1):
        puzzle.set(start_pos[0] + i + 1, size - start_pos[1] - 1, nb)
        nb += 1
        
    for i in range(size - 2 * start_pos[0] - 1):
        puzzle.set(size - start_pos[0] - 1, size - start_pos[1] - i - 2, nb)
        nb += 1
        
    for i in range(size - 2 * start_pos[1] - 2):
        puzzle.set(size - start_pos[0] - i - 2, start_pos[1], nb)
        nb += 1
    
    if start_pos[0] * 2 + 1 < size:
        start_pos[0] += 1
        start_pos[1] += 1
        puzzle = generate_puzzle(size, puzzle, start_pos, nb)
    else:
        puzzle.set(size//2, (size-1)//2, 0)
        
    return puzzle
 
def spiral(size, puzzle, start_pos=None, result=None):
    """
    reorder the puzzle array according to spiral:
    [1,2,3,8,0,4,7,6,5] => [1,2,3,4,5,6,7,8,0]
    """
    if result is None:
        result = []
    if start_pos is None:
        start_pos = [0, 0]

    puzzle = Puzzle(size, puzzle)

    for i in range(size - 2 * start_pos[0]):
        result.append(puzzle.get(start_pos[0], start_pos[1] + i))

    for i in range(size - 2 * start_pos[1] - 1):
        result.append(puzzle.get(start_pos[0] + i + 1, size - start_pos[1] - 1))

    for i in range(size - 2 * start_pos[0] - 1):
        result.append(puzzle.get(size - start_pos[0] - 1, size - start_pos[1] - i - 2))

    for i in range(size - 2 * start_pos[1] - 2):
        result.append(puzzle.get(size - start_pos[0] - i - 2, start_pos[1]))

    if start_pos[0] * 2 + 1 < size:
        start_pos[0] += 1
        start_pos[1] += 1
        puzzle = spiral(size, puzzle, start_pos, result)
    else:
        puzzle.set(size//2, (size-1)//2, 0)

    return result