#!/usr/bin/python3
import srcs.global_var as g
from srcs.heuristics import heuristic_list
from srcs.stats import get_stats, get_and_print_stats


class Puzzle(list):
    """
    puzzle format:
        for 3*3 puzzle
        [1, 2, 3, 8, 0, 4, 7, 6, 5]
    """
    def __init__(self, puzzle, parent=None, *args, **kwargs):
        list.__init__(self, *args, **kwargs)

        self.extend(puzzle)
        self.hash = hash(str(list(self)))
        self.last_move = None

        # saved info to avoid useless calcul
        self.parent = parent
        if parent is not None:
            self.dist_from_start = parent.dist_from_start
            self.dist_manhattan = parent.dist_manhattan
            self.dist_to_goal = parent.dist_to_goal
        else:
            self.dist_from_start = 0
            self.dist_manhattan = None
            self.dist_to_goal = None
        # position of 0 in the list (x, y)
        idx = self.index(0)
        self.pos0xy = [idx // g.param['size'], idx % g.param['size']]

    def __str__(self):
        s = ''
        for i in range(g.param['size']):
            for j in range(g.param['size']):
                nb = self.get(i, j)
                if nb == 0:
                    s += "%4s" % ("")
                else:
                    s += "%-3d " % (self.get(i, j))
            s += '\n'
        return s[:-1]

    def calc_heuristic(self):
        """
        calcul the heuristic of te puzzle
        """
        heuristic_list[g.param['heuristic']](self)

    def get(self, x, y):
        return self[x * g.param['size'] + y % g.param['size']]

    def set(self, x, y, val):
        self[x * g.param['size'] + y % g.param['size']] = val

    def updtHash(self):
        self.hash = hash(str(list(self)))

    def get_dist_from_goal(self, x, y=None):
        """
        take an index in argument and return his distance to the goal
        """
        if y is None:
            index = x
        else:
            index = x * g.param['size'] + y % g.param['size']
        val = self[index]
        if val == g.param['resolved_puzzle'][index] or val == 0:
            return 0  # is is well placed

        res_val = g.param['resolved_puzzle'].index(val)

        # abs(x - goal_x) + abs(y - goal_y)
        dist = abs(index // g.param['size'] - res_val // g.param['size']) + abs(index % g.param['size'] - res_val % g.param['size'])
        return dist

    def is_well_placed(self, x, y=None):
        """
        return True if the element is well placed
        """
        if y is None:
            index = x
        else:
            index = x * g.param['size'] + y % g.param['size']
        if g.param['resolved_puzzle'][index] == self[index] or self[index] == 0:
            return True
        return False

    def get_inversions(self, x1, y1=None):
        """
        get number of inversion on an element
        """
        inversions = 0
        if self.get(x1, y1) != 0:
            pos_col = self.is_in_column(x1, y1)
            if pos_col:
                list_upper = []  # list of all elements upper
                for x2 in range(pos_col[0]):
                    list_upper.append(g.param['resolved_puzzle'].get(x2, y1))
                for x2 in range(x1+1, g.param['size']):
                    if self.get(x2, y1) != 0:
                        if self.get(x2, y1) in list_upper:
                            inversions += 1

            pos_ln = self.is_in_line(x1, y1)
            if pos_ln:
                list_upper = []  # list of all elements upper
                for y2 in range(pos_ln[1]):
                    list_upper.append(g.param['resolved_puzzle'].get(x1, y2))
                for y2 in range(y1+1, g.param['size']):
                    if self.get(x1, y2) != 0:
                        if self.get(x1, y2) in list_upper:
                            inversions += 1
        return inversions

    def is_in_line(self, x, y=None):
        """
        if the element is in the right line, return his position
        """
        if y is None:
            y = x % g.param['size']
            x = x // g.param['size']

        val = self.get(x, y)
        for i in range(g.param['size']):
            if g.param['resolved_puzzle'].get(x, i) == val:
                return (x, i)
        return None

    def is_in_column(self, x, y=None):
        """
        if the element is in the right column, return his position
        """
        if y is None:
            y = x % g.param['size']
            x = x // g.param['size']

        val = self.get(x, y)
        for i in range(g.param['size']):
            if g.param['resolved_puzzle'].get(i, y) == val:
                return (i, y)
        return None

    def swap(self, x1, y1, x2, y2):
        """
        if heuristic == None -> don't update total dist
        swap 2 values
        return True if we can swap
        else return False
        """
        if min(x1, x2) < 0 or max(x1, x2) >= g.param['size'] or min(y1, y2) < 0 or max(y1, y2) >= g.param['size']:
            return False

        if g.param['auto_update_heuristic']:
            if g.param['heuristic'] == 'manhattan' and self.dist_manhattan is not None:
                # get the distance to goal for the 2 swapped point
                last_dist = self.get_dist_from_goal(x1, y1) + self.get_dist_from_goal(x2, y2)
            elif g.param['heuristic'] == 'hamming' and self.dist_to_goal is not None:
                last_dist = int(not self.is_well_placed(x1, y1)) + int(not self.is_well_placed(x2, y2))
            elif g.param['heuristic'] == 'linear_conflict' and self.dist_manhattan is not None:
                last_dist = self.get_dist_from_goal(x1, y1) + self.get_dist_from_goal(x2, y2)
                # last_inv = self.get_inversions(x1, y1) * 2 + self.get_inversions(x2, y2) * 2

        tmp = self.get(x1, y1)
        self.set(x1, y1, self.get(x2, y2))
        self.set(x2, y2, tmp)

        if self.get(x1, y1) == 0:
            self.pos0xy = [x1, y1]
        elif self.get(x2, y2) == 0:
            self.pos0xy = [x2, y2]

        if g.param['auto_update_heuristic']:
            if g.param['heuristic'] == 'manhattan' and self.dist_manhattan is not None:
                # get the distance to goal for the 2 swapped point
                new_dist = self.get_dist_from_goal(x1, y1) + self.get_dist_from_goal(x2, y2)
                # update dist to goal
                self.dist_manhattan = self.dist_manhattan - last_dist + new_dist
                self.dist_to_goal = self.dist_manhattan
            elif g.param['heuristic'] == 'hamming' and self.dist_to_goal is not None:
                new_dist = int(not self.is_well_placed(x1, y1)) + int(not self.is_well_placed(x2, y2))
                self.dist_to_goal = self.dist_to_goal - last_dist + new_dist
            elif g.param['heuristic'] == 'linear_conflict' and self.dist_manhattan is not None:
                new_dist = self.get_dist_from_goal(x1, y1) + self.get_dist_from_goal(x2, y2)
                new_inv = self.get_inversions(x1, y1) * 2 + self.get_inversions(x2, y2) * 2
                self.dist_manhattan = self.dist_manhattan - last_dist + new_dist
                # self.dist_to_goal = self.dist_manhattan - last_inv + new_inv
                self.dist_to_goal = None
                self.calc_heuristic()
            else:
                self.dist_to_goal = None
                self.dist_manhattan = None
                self.calc_heuristic()
        else:
            self.dist_to_goal = None
            self.dist_manhattan = None
            self.calc_heuristic()

        return True

    @get_stats
    def move(self, direction):
        """
        if heuristic is None -> dont update total dist
        move in one direction
            - T(op)
            - B(ottom)
            - L(eft)
            - R(ight)
        """
        if self.pos0xy is None:
            idx = self.index(0)
            self.pos0xy = [idx // g.param['size'], idx % g.param['size']]

        x = self.pos0xy[0]
        y = self.pos0xy[1]
        if direction == 'T':
            self.swap(x, y, x - 1, y)
        elif direction == 'B':
            self.swap(x, y, x + 1, y)
        elif direction == 'L':
            self.swap(x, y, x, y - 1)
        elif direction == 'R':
            self.swap(x, y, x, y + 1)
        else:
            print("[ERROR]: invalid move")
        self.last_move = direction
        if not g.param['super_fast']:
            self.dist_from_start += 1
        self.hash = hash(str(list(self)))
        return self

    def get_path(self):
        """
        get the entire path (LLTRBL...)
        """
        if self.parent is None:
            return ""
        return self.parent.get_path() + self.last_move

    def get_all_puzzles(self, list_puzzle=[]):
        """
        get the list of all puzzles
        """
        list_puzzle.insert(0, self)
        if self.parent is None:
            return list_puzzle
        return self.parent.get_all_puzzles(list_puzzle)


    # compare function <
    def __lt__(self, other):
        return (self.dist_from_start + (self.dist_to_goal if self.dist_to_goal is not None else 0)) < \
            (other.dist_from_start + (other.dist_to_goal if other.dist_to_goal is not None else 0))

    # compare function <=
    def __le__(self, other):
        return (self.dist_from_start + (self.dist_to_goal if self.dist_to_goal is not none else 0)) <= \
            (other.dist_from_start + (other.dist_to_goal if other.dist_to_goal is not none else 0))

    # compare function >=
    def __ge__(self, other):
        return (self.dist_from_start + (self.dist_to_goal if self.dist_to_goal is not None else 0)) >= \
            (other.dist_from_start + (other.dist_to_goal if other.dist_to_goal is not None else 0))

    # compare function >
    def __gt__(self, other):
        return (self.dist_from_start + (self.dist_to_goal if self.dist_to_goal is not None else 0)) > \
            (other.dist_from_start + (other.dist_to_goal if other.dist_to_goal is not None else 0))
