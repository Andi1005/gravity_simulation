import math

class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            return Vector2(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        else:
            return Vector2(self.x - other, self.y - other)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x / other, self.y / other)

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rtruediv__ = __truediv__

    def __str__(self):
        return f"{self.x}; {self.y}"

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    @staticmethod
    def distance(a, b):
        diff_vector = a - b
        return diff_vector.length()

    def to_float(self):
        return (self.x, self.y)

    def normalize(self):
        return self / self.length()
