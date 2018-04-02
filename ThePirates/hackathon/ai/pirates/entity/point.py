from __future__ import (
    absolute_import,
    unicode_literals,
)


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fire = False
        self.hit = False

    def is_fired(self):
        return self.fire

    def fire(self):
        self.fire = True

    def is_hit(self):
        return self.hit

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        """Override the default Unequal behavior"""
        return self.x != other.x or self.y != other.y

    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)
