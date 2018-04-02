import math

from hackathon.ai.pirates.entity.point import Point
from hackathon.ai.pirates.entity.ship import Ship
from settings import TypeOfShip


class FireHelper(object):
    @staticmethod
    def init_remain_ships(ship_info_arr):
        remain_ships = []
        for ship_info in ship_info_arr:
            for index in range(ship_info['quantity']):
                remain_ships.append(Ship(ship_info['type']))

        return remain_ships

    @staticmethod
    def remain_ship_type(remain_ships):
        remain_types = list(set([ship.type for ship in remain_ships]))
        # logger.info('Remain ship types: {}'.format(', '.join(remain_types)))
        return remain_types

    @staticmethod
    def create_probability_map(map_status, remain_ships, max_x, max_y):
        # reset map
        map_probability = [[0] * max_y for i in range(max_x)]
        for x in range(0, max_x):
            for y in range(0, max_y):
                if FireHelper.check_available_point(x, y, map_status):
                    point = Point(x, y)
                    # try to place ships
                    for ship_type in FireHelper.remain_ship_type(remain_ships):
                        map_probability = FireHelper.set_probability(ship_type, point, map_status, map_probability,
                                                                     max_x, max_y)
        print ''
        print 'Prob map: '
        print ''
        FireHelper.view_probability_map(map_probability, max_x, max_y, map_status)
        print ''

        return map_probability

    @staticmethod
    def view_probability_map(map_probability, width, height, map_status):
        for y in range(height - 1, -1, -1):
            line = 'y:' + str(y) + ' '
            for x in range(0, width):
                if map_status[x][y] == 0 and (x+y) % 2 == 0:
                    line += '  {}'.format(map_probability[x][y])
                else:
                    line += '   '

            print line
        print ''
        line = 'x:  '
        for x in range(0, width):
            line += '  ' + str(x)
        print line

        return line

    @staticmethod
    def set_probability(ship_type, point, map_status, map_probability, width, height):
        ship = Ship(ship_type, point, TypeOfShip.HORIZONTAL)
        map_probability = FireHelper.update_probability(ship.positions, map_status, map_probability, width, height)
        if ship_type != TypeOfShip.OIL_RIG:
            ship = Ship(ship_type, point, TypeOfShip.VERTICAL)
            map_probability = FireHelper.update_probability(ship.positions, map_status, map_probability, width, height)
        return map_probability

    @staticmethod
    def update_probability(points, map_status, map_probability, max_x, max_y):
        if FireHelper.check_fit_ship_in_map(points, map_status, max_x, max_y):
            for p in points:
                map_probability[p.x][p.y] += 1

        return map_probability

    @staticmethod
    def check_fit_ship_in_map(points, map_status, max_x, max_y):
        for point in points:
            if not FireHelper.check_usable_point(point, map_status, max_x, max_y):
                return False

        return True

    @staticmethod
    def clear_sunk_ship_points(hit_points, sink_ship):
        sink_positions = sink_ship.get('coordinates')
        for point in sink_positions:
            item = Point(point[0], point[1])
            if hit_points.count(item):
                hit_points.remove(item)

        return hit_points

    @staticmethod
    def update_remain_ships(sink_ship, remain_ships):
        for ship in remain_ships:
            if ship.type == sink_ship.get('type'):
                remain_ships.remove(ship)
                return remain_ships
        return remain_ships

    @staticmethod
    def check_usable_point(point, map_status, max_x, max_y):
        x = point.x
        y = point.y

        if x < 0 or x > (max_x - 1):
            return False
        if y < 0 or y > (max_y - 1):
            return False
        if not FireHelper.check_available_point(x, y, map_status):
            return False

        return True

    @staticmethod
    def check_available_point(x, y, map_status):
        return map_status[x][y] == 0

    @staticmethod
    def get_min_distance(remain_ships):
        remain_types = FireHelper.remain_ship_type(remain_ships)
        piece_arr = []
        for ship_type in remain_types:
            piece_arr.append(TypeOfShip.SHIP[ship_type]['pieces'])
        piece_arr = sorted(piece_arr, reverse=True)

        return piece_arr[0]

    @staticmethod
    def calculate_distance(x1, y1, x2, y2):
        return math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))
