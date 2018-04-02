from __future__ import (
    absolute_import,
    unicode_literals,
)
from hackathon.ai.pirates.entity.point import Point
from random import choice

from settings import TypeOfShip


class Ship(object):

    def __init__(self, ship_type, head=None, direct=None, start=None):
        self.type = ship_type
        self.head = head or Point(0, 0)
        self.ship_meta = TypeOfShip.SHIP[self.type]
        self.positions = []
        self.ship_direct = direct or self.init_direction()
        self.init_positions(start)

    def init_positions(self, start):
        ship_direct = self.ship_meta[self.ship_direct]
        start = start or ship_direct[0]
        for piece in ship_direct:
            x = self.head.x + piece['x'] - start['x']
            y = self.head.y + piece['y'] - start['y']
            self.positions.append(Point(x, y))

    def piece(self):
        return self.ship_meta['pieces']

    @staticmethod
    def init_direction():
        return choice(TypeOfShip.DIRECTION)

    # def __eq__(self, other):
    #     """Override the default Equals behavior"""
    #     return self.type == other.type
    #
    # def __ne__(self, other):
    #     """Override the default Unequal behavior"""
    #     return self.type != other.x.type
