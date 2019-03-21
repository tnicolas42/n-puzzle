import srcs.global_var as g


class Puzzle(list):
    """
    puzzle format:
        for 3*3 puzzle
        [1, 2, 3, 8, 0, 4, 7, 6, 5]
    """
    def __init__(self, size, puzzle, *args, **kwargs):
        list.__init__(self, *args, **kwargs)

        self.size = size
        self.extend(puzzle)

    def __str__(self):
        s = ''
        for i in range(self.size):
            for j in range(self.size):
                s += "%-3d " % (self.get(i, j))
            s += '\n'
        return s[:-1]

    def get(self, x, y):
        return self[x * self.size + y % self.size]

    def set(self, x, y, val):
        self[x * self.size + y % self.size] = val

    def get_dist_from_goal(self, x, y=None):
        """
        take an index in argument and return his distance to the goal
        """
        if y is None:
            index = x
        else:
            index = x * self.size + y % self.size
        val = self[index]
        if val == g.resolved_puzzle[index]:
            return 0  # is is well placed

        for i in range(g.total_size):
            if g.resolved_puzzle[i] == val:
                break

        # dist = abs(x - goal_x) + abs(y - gaol_y)
        dist = abs(index // self.size - i // self.size) + abs(index % self.size - i % self.size)
        return dist
