from random import (
    randint,
    randrange
)
from hackathon.ai.pirates.entity.point import Point


class BoardHelper(object):

    @staticmethod
    def is_occupied(point, occupied):
        for allocated in occupied:
            if allocated.x == point.x and allocated.y == point.y:
                return True
        return False

    @staticmethod
    def random_position(width, height):
        x = randint(0, width - 1)
        y = randint(0, height - 1)
        return Point(x, y)

    @staticmethod
    def get_near_positions(position, width, height):
        near_positions = [Point(position.x, position.y + 1),
                          Point(position.x, position.y - 1),
                          Point(position.x + 1, position.y),
                          Point(position.x - 1, position.y)]
        return [near for near in near_positions if BoardHelper.is_valid_position(near, width, height)]

    @staticmethod
    def is_valid_position(position, width, height):
        if position.x >= width or position.y >= height:
            return False
        if position.x < 0 or position.y < 0:
            return False
        return True

    @staticmethod
    def is_stick_position(position, allocates, width, height):
        """
        A position is nice when it does not near any ships.
        :param position: A position need to check
        :return:
        """
        nears_position = BoardHelper.get_near_positions(position, width, height)
        if BoardHelper.is_double_occupied(nears_position, allocates):
            return True
        return False

    @staticmethod
    def is_double_occupied(positions, occupied):
        for position in positions:
            if BoardHelper.is_occupied(position, occupied):
                return True
        return False

    @staticmethod
    def pick_random(available):
        index = randrange(len(available))
        return available[index]

    @staticmethod
    def remove_position(position, occupied):
        for allocated in occupied:
            if allocated.x == position.x and allocated.y == position.y:
                occupied.remove(allocated)

    @staticmethod
    def remove_occupied(positions, occupied):
        return [position for position in positions if not BoardHelper.is_occupied(position, occupied)]
