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
        self.parent = None  # None only for the base puzzle
        self.last_move = None

        # saved info to avoid useless calcul
        self.dist_from_start = 0
        self.dist_to_goal = None

    def init_child(self, parent):
        self.parent = parent

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

        res_val = g.resolved_puzzle.index(val)

        # dist = abs(x - goal_x) + abs(y - gaol_y)
        dist = abs(index // self.size - res_val // self.size) + abs(index % self.size - res_val % self.size)
        return dist

    def swap(self, x1, y1, x2, y2, heuristic=None):
        """
        if heuristic == None -> don't update total dist
        swap 2 values
        return True if we can swap
        else return False
        """
        if min(x1, x2) < 0 or max(x1, x2) >= self.size or min(y1, y2) < 0 or max(y1, y2) >= self.size:
            return False

        if heuristic is None or self.dist_to_goal is None:
            # reset the dist to goal
            self.dist_to_goal = None
        else:
            if heuristic == 'manhattan':
                # get the distance to goal for the 2 swapped point
                last_dist = self.get_dist_from_goal(x1, y1) + self.get_dist_from_goal(x2, y2)
            else:
                print("cannot update total_dist with heuristic %s" % heuristic)
                # reset the dist to goal
                self.dist_to_goal = None

        tmp = self.get(x1, y1)
        self.set(x1, y1, self.get(x2, y2))
        self.set(x2, y2, tmp)

        if heuristic is not None and self.dist_to_goal is not None:
            if heuristic == 'manhattan':
                # get the distance to goal for the 2 swapped point
                new_dist = self.get_dist_from_goal(x1, y1) + self.get_dist_from_goal(x2, y2)
                # update dist to goal
                self.dist_to_goal = self.dist_to_goal - last_dist + new_dist
        return True

    def move(self, direction, heuristic=None):
        """
        if heuristic is None -> dont update total dist
        move in one direction
            - T(op)
            - B(ottom)
            - L(eft)
            - R(ight)
        """
        idx = self.index(0)
        x = idx // self.size
        y = idx % self.size
        if direction == 'T':
            self.swap(x, y, x-1, y, heuristic=heuristic)
        elif direction == 'B':
            self.swap(x, y, x+1, y, heuristic=heuristic)
        elif direction == 'L':
            self.swap(x, y, x, y-1, heuristic=heuristic)
        elif direction == 'R':
            self.swap(x, y, x, y+1, heuristic=heuristic)
        else:
            print("[ERROR]: invalid move")
        self.last_move = direction
        self.dist_from_start += 1
        return self

    def get_path(self):
        if self.parent is None:
            return ""
        return self.parent.get_path() + self.last_move
