class Puzzle(list):
    def __init__(self, size, puzzle, *args, **kwargs):
        list.__init__(self, *args, **kwargs)

        self.size = size
        self.extend(puzzle)

    def __str__(self):
        s = ''
        for i in range(self.size):
            for j in range(self.size):
                s += "%-4d" % (self.get(i, j))
            s += '\n'
        return s[:-1]

    def get(self, x, y):
        return self[x * self.size + y % self.size]

    def set(self, x, y, val):
        self[x * self.size + y % self.size] = val
