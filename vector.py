class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        if isinstance(other, tuple):
            return Vector(self.x + other[0], self.y + other[1])
        return Vector(self.x + other.x, self.y + other.y)
    def __iadd__(self, other):
        if isinstance(other, tuple):
            return Vector(self.x + other[0], self.y + other[1])
        return Vector(self.x + other.x, self.y + other.y)
    def __str__(self):
        return str((self.x, self.y))
    def __repr__(self):
        return repr((self.x, self.y))
    def __eq__(self, other):
        if isinstance(other, tuple):
            return self.x == other[0] and self.y == other[1]
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y
    def __invert__(self):
        return Vector(-self.x, -self.y)
    def __sub__(self, other):
        if isinstance(other, tuple):
            return Vector(self.x - other[0], self.y - other[1])
        return Vector(self.x - other.x, self.y - other.y)
    def to_tuple(self):
        return (self.x, self.y)
    def direction(self):
        return Vector(cmp(self.x, 0), cmp(self.y, 0))
