from __future__ import annotations
import functools
import math


class Size:
    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols


@functools.total_ordering
class Coordinate:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def normalize(self):
        d = math.gcd(self.x, self.y)
        return self // d

    def in_range(self, size: Size) -> bool:
        return 0 <= self.x < size.rows and 0 <= self.y < size.cols

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.x < other.x if self.x != other.x else self.y < other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(self.x * other.x, self.y * other.y)
        if isinstance(other, int):
            return Coordinate(self.x * other, self.y * other)
        raise NotImplementedError(f"Multiplication not defined for {type(other)}")

    def __floordiv__(self, other):
        if isinstance(other, int):
            return Coordinate(self.x // other, self.y // other)
        raise NotImplementedError(f"Division not defined for {type(other)}")

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __str__(self):
        return f"({self.x},{self.y})"
