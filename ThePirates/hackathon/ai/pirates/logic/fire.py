import random

from hackathon.ai.pirates.entity.point import Point
from hackathon.ai.pirates.entity.ship import Ship
from hackathon.ai.pirates.utils.board_helper import BoardHelper
from hackathon.ai.pirates.utils.fire_helper import FireHelper
from settings import TypeOfShip, AiConfig, FireMode


class FireLogic(object):
    @staticmethod
    def fire(remain_ships, map_status, hit_points, map_probability, max_x, max_y, history_hit, prioritize_shots, max_shots=1):
        if AiConfig.FIRE_MODE == FireMode.RANDOM:
            points = FireLogic.get_random_point(max_x, max_y)
        else:
            if not hit_points:
                # HUNT MODE
                fire_point = []
                if AiConfig.HISTORY_MODE and (max_shots == 1 or max_shots < AiConfig.MAX_SAVING_SHOTS):
                    fire_point, history_hit = FireLogic.get_history_shot(map_status, history_hit, map_probability, max_x, max_y)
                if fire_point:
                    print 'HISTORY HIT is : {}'.format(fire_point)
                    points = [
                        [fire_point.x, fire_point.y]
                    ]
                    return points, history_hit, prioritize_shots
                # 25% shot in prioritize shots
                if random.choice([True]*AiConfig.PRIORITY_CHANGE + [False]*(100 - AiConfig.PRIORITY_CHANGE)) \
                        and (max_shots == 1 or max_shots < AiConfig.MAX_SAVING_SHOTS):
                    fire_point, prioritize_shots = FireLogic.get_prioritize_shot(map_status, prioritize_shots, map_probability, max_x, max_y)
                if fire_point:
                    print 'PRIORITIZE SHOTS is : {}'.format(fire_point)
                    points = [
                        [fire_point.x, fire_point.y]
                    ]
                    return points, history_hit, prioritize_shots
                points = FireLogic.get_fire_point_by_probability(remain_ships, map_status, map_probability, max_x, max_y, max_shots)
            else:
                # TARGET MODE
                points = FireLogic.target_mode(hit_points, remain_ships, map_status,  max_x, max_y)

        return points, history_hit, prioritize_shots

    @staticmethod
    def get_history_shot(map_status, history_hits, map_probability, max_x, max_y):
        while history_hits:
            fire_point = history_hits.pop()
            if FireHelper.check_usable_point(fire_point, map_status, max_x, max_y) and map_probability[fire_point.x][fire_point.y] > 0:
                return fire_point, history_hits
        return [], history_hits

    @staticmethod
    def get_prioritize_shot(map_status, prioritize_shots, map_probability, max_x, max_y):
        while prioritize_shots:
            fire_point = prioritize_shots.pop()
            fire_point = Point(fire_point['x'], fire_point['y'])
            if FireHelper.check_usable_point(fire_point, map_status, max_x, max_y) and map_probability[fire_point.x][fire_point.y] > 0:
                return fire_point, prioritize_shots
        return [], prioritize_shots

    @staticmethod
    def get_fire_point_by_probability(remain_ships, map_status, map_probability, max_x, max_y, max_shots):
        highest_prob = 0
        next_points = []
        avail_points = []
        fire_points = []
        for x in range(0, max_x):
            for y in range(0, max_y):
                if (x + y) % 2 == 0 and FireHelper.check_available_point(x, y, map_status):
                    avail_points.append(Point(x, y))
                    if map_probability[x][y] > highest_prob:
                        # empty current list and add item to list
                        highest_prob = map_probability[x][y]
                        del next_points[:]
                        next_points.append(Point(x, y))
                    elif map_probability[x][y] == highest_prob:
                        next_points.append(Point(x, y))

        # choose random in list
        if max_shots == 1 or max_shots < AiConfig.MAX_SAVING_SHOTS:
            fire_point = random.choice(next_points)
            fire_points = [
                [fire_point.x, fire_point.y]
            ]
        else:
            # do combo shots
            # 1. sort by probability value: x1 >= x2 >= x3 ..
            avail_points.sort(key=lambda item: map_probability[item.x][item.y], reverse=True)
            fire_point = avail_points[0]
            fire_points.append([fire_point.x, fire_point.y])
            number_of_shot = max_shots - 1

            # 2. calculate distance to 1st point
            distance_arr = []
            for i in range(0, len(avail_points)):
                distance_arr.append(FireHelper.calculate_distance(fire_point.x, fire_point.y, avail_points[i].x,
                                                                  avail_points[i].y))
            # 3. get next points base on min_distance
            min_distance = FireHelper.get_min_distance(remain_ships)
            print 'min_distance: {}'.format(min_distance)
            points = FireLogic.get_shot_by_min_distance(avail_points, distance_arr, min_distance, number_of_shot)

            fire_points += points

        return fire_points

    @staticmethod
    def get_shot_by_min_distance(avail_points, distance_arr, min_distance, number_of_shot):
        points = []
        for i in range(0, len(distance_arr)):
            if distance_arr[i] >= min_distance:
                points.append([avail_points[i].x, avail_points[i].y])
                if len(points) == number_of_shot:
                    return points
        # try decrease distance to get more points
        delta = min_distance - 1

        return FireLogic.get_shot_by_min_distance(avail_points, distance_arr, delta,
                                                  number_of_shot) if delta > 0 else []

    @staticmethod
    def target_mode(hit_points, remain_ship, map_status,  max_x, max_y):
        remain_positions = []
        remain = FireHelper.remain_ship_type(remain_ship)
        print 'Remain ship types: {}'.format(', '.join([ship.type for ship in remain_ship]))
        for delta in range(0, len(hit_points)):
            for position in hit_points:
                for ship_type in remain:
                    ship_direct = FireLogic.get_ship_direct()
                    for ship_start in TypeOfShip.SHIP[ship_type][ship_direct[0]]:
                        ship = Ship(ship_type, position, ship_direct[0], ship_start)
                        remain_position = FireLogic.get_remain_position(map_status, hit_points, ship, delta, max_x, max_y)
                        if remain_position:
                            remain_positions.append(remain_position)
                    for ship_start in TypeOfShip.SHIP[ship_type][ship_direct[1]]:
                        ship = Ship(ship_type, position, ship_direct[1], ship_start)
                        remain_position = FireLogic.get_remain_position(map_status, hit_points, ship, delta, max_x, max_y)
                        if ship_type != TypeOfShip.OIL_RIG and remain_position:
                            remain_positions.append(remain_position)
            if remain_positions:
                # logger.info('Remain positions: {} after {} attempt'.format(len(remain_positions), delta))
                break
        remain_positions.sort(key=lambda tub: len(tub))
        FireLogic.render_position(remain_positions, max_x, max_y, hit_points, map_status)
        return [
            [remain_positions[0][0].x, remain_positions[0][0].y]
        ]

    @staticmethod
    def get_ship_direct():
        ship_direct = [TypeOfShip.HORIZONTAL, TypeOfShip.VERTICAL]
        random.shuffle(ship_direct)
        return ship_direct

    @staticmethod
    def render_position(positions, width, height, hit_points, map_status):
        remain = positions[0] if positions else []
        for y in range(height-1, -1, -1):
            line = 'y:' + str(y) + ' '
            for x in range(0, width):
                if BoardHelper.is_occupied(Point(x, y), remain):
                    line += '  v'
                elif BoardHelper.is_occupied(Point(x, y), hit_points):
                    line += '  o'
                elif map_status[x][y] == 9:
                    line += '  h'
                elif map_status[x][y] == 1:
                    line += '  x'
                else:
                    line += '   '

            print line
        line = 'x:  '
        for x in range(0, width):
            line += '  ' + str(x)
        print line

        return line

    @staticmethod
    def get_remain_position(map_status, hit_points, ship, delta, max_x, max_y):
        """
        Check position of ship is valid on board or not
        And position of this ship is fire but not hit
        And must one piece of ship is not fire yet
        :param map_status:
        :param hit_points:
        :param ship:
        :param delta:
        :param max_x:
        :param max_y:
        :return:
        """
        remain_position = []
        # Get hit position which is not in ship
        remain_hit = BoardHelper.remove_occupied(hit_points, ship.positions)
        if len(remain_hit) > delta:
            return remain_position

        # Validate this ship is valid or not
        for position in ship.positions:
            # Does not outside board
            if not BoardHelper.is_valid_position(position, max_x, max_y):
                return []

            if position in hit_points:
                continue
            elif map_status[position.x][position.y] == 9 or map_status[position.x][position.y] == 1:
                return []

            # Add positions which is not fire  yet
            if map_status[position.x][position.y] == 0:
                remain_position.append(position)
        # logger.debug('Match ship type: {}'.format(ship.type))
        return remain_position

    # def get_nearby_positions(hit_points):
    #     high_expect_positions = []
    #     if hit_points:
    #         for position in hit_points:
    #             near_positions = get_near_positions(position, self.width, self.height)
    #             high_expect_positions = remove_occupied_position(near_positions, self.fired_positions)
    #             if high_expect_positions:
    #                 break
    #     if not high_expect_positions:
    #         logger.error('Find nearby fail.')
    #         return None
    #     return pick_random(high_expect_positions)

    @staticmethod
    def get_random_point(max_x, max_y):
        x = random.randint(0, max_x - 1)

        # even
        if x % 2 == 0:
            y = random.choice(range(0, max_y, 2))
        else:
            y = random.choice(range(1, max_y, 2))

        return [[x, y]]
