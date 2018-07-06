from typing import Tuple

import numpy as np
import math


class Point2D:
    def __init__(self, x_init, y_init):
        self.x = x_init
        self.y = y_init

    def as_tuple(self):
        return self.x, self.y

    def as_int_tuple(self):
        return int(self.x), int(self.y)

    def shift(self, x, y):
        self.x += x
        self.y += y

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])

    def distance_from(self, other_point: 'Point2D') -> float:
        return math.sqrt((self.x - other_point.x) ** 2 + (self.y - other_point.y) ** 2)

    def closest_point_in_list(self, *points: Tuple['Point2D']):
        distances = [self.distance_from(point) for point in points]
        idx = np.argmin(distances)
        return points[idx], idx

    def __json_encode__(self):
        return self.__dict__

    def __json_decode__(self, **attrs):
        self.x = attrs['x']
        self.y = attrs['y']


class Rectangle:

    def __init__(self, upper_left: Point2D, bottom_right: Point2D) -> None:
        self.upper_left = upper_left
        self.bottom_right = bottom_right
        self.height = bottom_right.y - upper_left.y
        self.width = bottom_right.x - upper_left.x

    def surface(self) -> float:
        return self.height * self.width

    def center(self):
        return Point2D(self.upper_left.x + self.width / 2.0, self.upper_left.y + self.height / 2.0)

    def contains(self, point: Point2D):
        return self.upper_left.x < point.x < self.bottom_right.x and self.upper_left.y < point.y < self.bottom_right.y

    def distance_from_point(self, point: Point2D):
        # You can clamp to the nearest point in the rectangle, and find the distance to that point.
        #  The nearest point on the rectangle is given by
        nearest_point_in_rect = Point2D(point.x, point.y)
        if point.x < self.upper_left.x:
            nearest_point_in_rect.x = self.upper_left.x
        elif point.x > self.bottom_right.x:
            nearest_point_in_rect.x = self.bottom_right.x

        if point.y < self.upper_left.y:
            nearest_point_in_rect.y = self.upper_left.y
        elif point.y > self.bottom_right.y:
            nearest_point_in_rect.y = self.bottom_right.y

        return nearest_point_in_rect.distance_from(point)

    def __json_encode__(self):
        return self.__dict__

    def __json_decode__(self, attrs):
        self.upper_left = attrs['upper_left']
        self.bottom_right = attrs['bottom_right']
        self.width = attrs['width']
        self.height = attrs['height']

    @classmethod
    def from_center_and_dimension(cls, center: Point2D, width, height):
        upper_left = Point2D(center.x - width / 2.0, center.y - height / 2.0)
        bottom_right = Point2D(center.x + width / 2.0, center.y + height / 2.0)
        return cls(upper_left, bottom_right)
