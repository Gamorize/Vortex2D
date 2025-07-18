from base import Component
from math import sqrt

class Vector2D(Component):
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def magnitude(self):
        return sqrt(self.x ** 2 + self.y ** 2)
