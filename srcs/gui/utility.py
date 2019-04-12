class Point:
    """
        2d Point class
    """

    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def move(self, shift):
        """ move x and y move """
        self.X = self.X + shift.x
        self.Y = self.Y + shift.y

    def __str__(self):
        return "Point(%s,%s)"%(self.X, self.Y) 

    def X(self):
        return self.X

    def Y(self):
        return self.Y

    def __sub__(self, other):
        return Point(self.X - other.X, self.Y - other.Y)