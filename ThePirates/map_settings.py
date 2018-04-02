from settings import TypeOfShip

MAP_1 = [
    {
        'type': TypeOfShip.DESTROYER,
        'pos': {'x': 0, 'y': 1},
        'direction': TypeOfShip.VERTICAL
    },
    {
        'type': TypeOfShip.DESTROYER,
        'pos': {'x': 19, 'y': 1},
        'direction': TypeOfShip.VERTICAL
    },
    {
        'type': TypeOfShip.DESTROYER,
        'pos': {'x': 5, 'y': 0},
        'direction': TypeOfShip.HORIZONTAL
    },
    {
        'type': TypeOfShip.CRUISER,
        'pos': {'x': 19, 'y': 5},
        'direction': TypeOfShip.VERTICAL
    },
]

MAP_2 = [
    {
        'type': TypeOfShip.DESTROYER,
        'pos': {'x': 15, 'y': 7},
        'direction': TypeOfShip.HORIZONTAL
    },
    {
        'type': TypeOfShip.CRUISER,
        'pos': {'x': 14, 'y': 0},
        'direction': TypeOfShip.HORIZONTAL
    },
    {
        'type': TypeOfShip.CRUISER,
        'pos': {'x': 2, 'y': 7},
        'direction': TypeOfShip.HORIZONTAL
    }
]

PLAYER_MAP = {
    'ea_team_no1': {
        'map': [MAP_1, MAP_2],
        'direction': TypeOfShip.HORIZONTAL,
        'prioritize-shot': [{'x': 4, 'y': 7}, {'x': 17, 'y': 2}, {'x': 17, 'y': 0}, {'x': 17, 'y': 7}],
        'percent': 50
    },
    '4t': {
        'map': [MAP_1, MAP_2],
        'direction': TypeOfShip.HORIZONTAL,
        'prioritize-shot': [],
        'percent': 50
    },
    'default': {
        'map': [MAP_1, MAP_2],
        'direction': TypeOfShip.HORIZONTAL,
        'prioritize-shot': [{'x': 1, 'y': 0}, {'x': 19, 'y': 6}, {'x': 1, 'y': 7}, {'x': 0, 'y': 1}],
        'percent': 50
    },
}
