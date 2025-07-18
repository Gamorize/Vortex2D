from base import Component
import math

class Box2D(Component):
    def __init__(self, point1, point2):
        self._point1 = point1
        self._point2 = point2
        self._calculate_properties()

    def _calculate_properties(self):
        x1, y1 = self._point1
        x2, y2 = self._point2
        self.x_min, self.x_max = min(x1, x2), max(x1, x2)
        self.y_min, self.y_max = min(y1, y2), max(y1, y2)
        self.width = self.x_max - self.x_min
        self.height = self.y_max - self.y_min
        self.area = self.width * self.height
        self.middle_point = ((self.x_min + self.x_max) / 2, (self.y_min + self.y_max) / 2)

    @property
    def point1(self):
        return self._point1

    @point1.setter
    def point1(self, value):
        self._point1 = value
        self._calculate_properties()

    @property
    def point2(self):
        return self._point2

    @point2.setter
    def point2(self, value):
        self._point2 = value
        self._calculate_properties()

class Polygon2D(Component):
    def __init__(self, points):
        self._points = points
        self._calculate_properties()

    def _calculate_properties(self):
        xs, ys = zip(*self._points)
        self.x_min, self.x_max = min(xs), max(xs)
        self.y_min, self.y_max = min(ys), max(ys)
        self.width = self.x_max - self.x_min
        self.height = self.y_max - self.y_min
        self.area = self._calculate_area()
        self.middle_point = ((self.x_min + self.x_max) / 2, (self.y_min + self.y_max) / 2)

    def _calculate_area(self):
        area = 0
        points = self._points
        for i in range(len(points)):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)]
            area += x1 * y2 - y1 * x2
        return abs(area) / 2

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        self._points = value
        self._calculate_properties()

class Circle2D(Component):
    def __init__(self, center, radius):
        self._center = center
        self._radius = radius
        self._calculate_properties()

    def _calculate_properties(self):
        self.x, self.y = self._center
        self.area = math.pi * self._radius ** 2
        self.middle_point = self._center

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        self._center = value
        self._calculate_properties()

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value
        self._calculate_properties()

class Triangle2D(Component):
    def __init__(self, point1, point2, point3):
        self._points = [point1, point2, point3]
        self._calculate_properties()

    def _calculate_properties(self):
        xs, ys = zip(*self._points)
        self.x_min, self.x_max = min(xs), max(xs)
        self.y_min, self.y_max = min(ys), max(ys)
        self.width = self.x_max - self.x_min
        self.height = self.y_max - self.y_min
        self.area = self._calculate_area()
        self.middle_point = (
            sum(x for x, _ in self._points) / 3,
            sum(y for _, y in self._points) / 3
        )

    def _calculate_area(self):
        x1, y1 = self._points[0]
        x2, y2 = self._points[1]
        x3, y3 = self._points[2]
        return abs(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) / 2

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        if len(value) != 3:
            raise ValueError("Triangle requires exactly 3 points.")
        self._points = value
        self._calculate_properties()
