class AppConfig(object):
    app_host = '0.0.0.0'
    app_port = 5001
    app_debug = True
    redis_url = 'localhost'
    redis_port = 6379
    redis_db = 0
    mongo_host = '10.10.20.143'
    mongo_port = 27017
    mongo_db = 'the_pirates'


class FireMode(object):
    RANDOM = 'random'
    PROB = 'probability'


class GameConfig(object):
    HIT = 'HIT'
    MISS = 'MISS'
    PLAYER_ID = 'the_pirates'


class CacheConfig(object):
    BOARD_PREFIX = 'board_'
    HISTORY_HIT_PREFIX = 'history_hit_'
    PRIORITIZE_SHOTS_PREFIX = 'prioritize_shots_'
    MAP_STATUS_PREFIX = 'map_status_'
    SHIP_INFO_PREFIX = 'ship_info_'
    SHIP_REMAIN_PREFIX = 'ship_remain_'
    MAP_PROBABILITY_SUFFIX = 'map_probability_'
    COMPETITOR_MAP_PREFIX = 'competitor_map_'
    COMPETITOR_ID_PREFIX = 'competitor_id_'
    QUEUE_PREFIX = 'queue_'
    HIT_POINTS_PREFIX = 'hp_'


class AiConfig(object):
    MAP_STATUS_AVAILABLE = 0
    MAP_STATUS_MISS = 1
    MAP_STATUS_HIT = 9

    MAX_ATTEMPT = 500

    # 0: Stick
    # 10: 1/10 Ship stick
    # 1000: Never stick
    STICK_MODE = 1000

    HISTORY_MODE = True

    PRIORITY_CHANGE = 30

    MAX_SAVING_SHOTS = 2
    FIRE_MODE = FireMode.PROB


class TypeOfShip(object):
    CARRIER = 'CV'
    BATTLE_SHIP = 'BB'
    OIL_RIG = 'OR'
    CRUISER = 'CA'
    DESTROYER = 'DD'

    VERTICAL = 'VER'
    HORIZONTAL = 'HOR'

    DIRECTION = [HORIZONTAL, VERTICAL]

    SHIP = {
        CARRIER: {
            'pieces': 5,
            HORIZONTAL: [
                {'x': 0, 'y': 1},
                {'x': 1, 'y': 1},
                {'x': 2, 'y': 1},
                {'x': 3, 'y': 1},
                {'x': 1, 'y': 0}
            ],
            VERTICAL: [
                {'x': 1, 'y': 0},
                {'x': 1, 'y': 1},
                {'x': 1, 'y': 2},
                {'x': 1, 'y': 3},
                {'x': 0, 'y': 1},
            ]
        },
        BATTLE_SHIP: {
            'pieces': 4,
            HORIZONTAL: [
                {'x': 0, 'y': 0},
                {'x': 1, 'y': 0},
                {'x': 2, 'y': 0},
                {'x': 3, 'y': 0}
            ],
            VERTICAL: [
                {'x': 0, 'y': 0},
                {'x': 0, 'y': 1},
                {'x': 0, 'y': 2},
                {'x': 0, 'y': 3}
            ]
        },
        CRUISER: {
            'pieces': 3,
            HORIZONTAL: [
                {'x': 0, 'y': 0},
                {'x': 1, 'y': 0},
                {'x': 2, 'y': 0}
            ],
            VERTICAL: [
                {'x': 0, 'y': 0},
                {'x': 0, 'y': 1},
                {'x': 0, 'y': 2}
            ]
        },
        DESTROYER: {
            'pieces': 2,
            HORIZONTAL: [
                {'x': 0, 'y': 0},
                {'x': 1, 'y': 0}
            ],
            VERTICAL: [
                {'x': 0, 'y': 0},
                {'x': 0, 'y': 1}
            ]
        },
        OIL_RIG: {
            'pieces': 4,
            HORIZONTAL: [
                {'x': 0, 'y': 0},
                {'x': 0, 'y': 1},
                {'x': 1, 'y': 0},
                {'x': 1, 'y': 1}
            ],
            VERTICAL: [
                {'x': 0, 'y': 0},
                {'x': 0, 'y': 1},
                {'x': 1, 'y': 0},
                {'x': 1, 'y': 1}
            ]
        }
    }
