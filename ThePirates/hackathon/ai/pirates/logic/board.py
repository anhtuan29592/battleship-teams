from __future__ import (
    absolute_import,
    unicode_literals,
)

from hackathon.ai.pirates.entity.point import Point
from hackathon.ai.pirates.entity.ship import Ship
from hackathon.ai.pirates.utils.board_helper import BoardHelper
from random import (
    randint,
    choice
)

from map_settings import PLAYER_MAP
from settings import (
    AiConfig,
    TypeOfShip
)


class Board(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_ship = []
        self.allocates = []
        self.handmade_ship = []
        self.player_setting = {}

    def init_board(self, ships, player):
        self.init_player_settings(player)
        # convert request type to list
        # Exp {"type": "BB", "quantity": 4} -> ['BB', 'BB', 'BB', 'BB']
        ships_data = self.get_ships_data(ships)

        # Init handmade ship from map
        ships_data = self.init_handmade_ship(ships_data)

        for ship_type in ships_data:
            ship = self.init_ship(ship_type)
            # can not init ship after 500 times attempt
            # re-init whole board
            if not ship:
                self.allocates = []
                self.current_ship = []
                return self.init_board(ships, player)
            self.allocates.extend(ship.positions)
            self.current_ship.append(ship)

    def init_ship(self, ship_type):
        """
        Ship meta type ``BB``
        :param ship_type:
        :return:
        """
        # try to init ship in 500 times
        for i in range(0, AiConfig.MAX_ATTEMPT):
            # random head position of ship
            ship_head = BoardHelper.random_position(self.width, self.height)
            # from this head random direction of ship
            # and init whole ship data
            ship_direct = self.get_direction()
            ship = Ship(ship_type, ship_head, direct=ship_direct)

            # check position of ship is valid or not
            if self.is_nice_ship(ship):
                return ship
        else:
            return None

    def is_nice_ship(self, ship):
        """
        Check position of ship is overlap other ship or not.
        Optional: support nice position
        :param ship:
        :return:
        """
        for piece in ship.positions:
            # Does not outside board
            if not BoardHelper.is_valid_position(piece, self.width, self.height):
                return False
            # Does not overlap other ship
            if BoardHelper.is_occupied(piece, self.allocates):
                return False
            # Does not near any ship
            if randint(0, AiConfig.STICK_MODE) and BoardHelper.is_stick_position(piece, self.allocates, self.width, self.height):
                return False
        return True

    def is_valid_ship(self, ship):
        """
        Check position of ship is overlap other ship or not.
        Optional: support nice position
        :param ship:
        :return:
        """
        for piece in ship.positions:
            # Does not outside board
            if not BoardHelper.is_valid_position(piece, self.width, self.height):
                return False
            # Does not overlap other ship
            if BoardHelper.is_occupied(piece, self.allocates):
                return False
        return True

    def init_player_settings(self, player):
        player_settings = PLAYER_MAP.get(str(player)) or PLAYER_MAP.get('default')
        if player_settings:
            self.player_setting = player_settings
            player_map = player_settings.get('map')
            self.handmade_ship = BoardHelper.pick_random(player_map)

    def get_direction(self):
        percent = self.player_setting.get('percent', 50)
        return choice([TypeOfShip.HORIZONTAL]*percent + [TypeOfShip.VERTICAL]*(100 - percent))

    def init_handmade_ship(self, ships_data):
        for ship_meta in self.handmade_ship:
            if ship_meta['type'] in ships_data:
                ship = Ship(ship_meta['type'], Point(ship_meta['pos']['x'], ship_meta['pos']['y']), direct=ship_meta['direction'])
                if self.is_valid_ship(ship):
                    self.allocates.extend(ship.positions)
                    self.current_ship.append(ship)
                    ships_data.remove(ship_meta['type'])
        return ships_data

    def get_ships_data(self, ships):
        ship_list = []
        for ship_data in ships:
            ship_list.extend([ship_data['type'] for index in range(int(ship_data['quantity']))])
        return ship_list

    def get_placed_ships_to_response(self):
        ships = []
        for ship in self.current_ship:
            ships.append({
                'type': ship.type,
                'coordinates': [[position.x, position.y] for position in ship.positions]
            })

        return ships

    def preview_placed_ships(self):
        for y in range(self.height, -1, -1):
            line = ''
            for x in range(0, self.width):
                is_allocated = BoardHelper.is_occupied(Point(x, y), self.allocates)
                point = 'x' if is_allocated else ' '
                line = line + ' ' + point

            print line
