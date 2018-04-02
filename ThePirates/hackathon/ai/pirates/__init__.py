from settings import AiConfig


class Point(object):
    """ Point class represents and manipulates x,y coords. """

    def __init__(self, x, y):
        """ Create a new point by new x, y """
        self.x = x
        self.y = y

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        """Override the default Unequal behavior"""
        return self.x != other.x or self.y != other.y

    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

    def get_response_data(self):
        return {
            'x': self.x,
            'y': self.y
        }


class Location(object):

    def __init__(self):
        self.point = Point()
        self.direction = AiConfig.HORIZONTAL

    def __init__(self, point, direction):
        self.point = point
        self.direction = direction


# class Ship(object):
#
#     def __init__(self, ship_type, quantity):
#         self.ship_type = ship_type
#         self.quantity = quantity
