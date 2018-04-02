from collections import deque

import pymongo as pymongo
import redis as redis
from flask import Flask, request

from hackathon.ai.api import ApiResponse, ApiInviteRequest, ApiPlaceShipsRequest, ApiShootRequest, ApiNotifyRequest, \
    ApiRequest
from hackathon.ai.pirates.entity.point import Point
from hackathon.ai.pirates.logic.board import Board
from hackathon.ai.pirates.logic.fire import FireLogic
from hackathon.ai.pirates.utils.cache_helper import CacheHelper
from hackathon.ai.pirates.utils.data_collector import DataCollector
from hackathon.ai.pirates.utils.fire_helper import FireHelper
from settings import GameConfig, AiConfig, AppConfig
from map_settings import PLAYER_MAP

app = Flask(__name__)
db = redis.Redis(host=AppConfig.redis_url, port=AppConfig.redis_port, db=AppConfig.redis_db)
mongo = pymongo.MongoClient(AppConfig.mongo_host, AppConfig.mongo_port)[AppConfig.mongo_db]
data_collector = DataCollector(mongo)


@app.route('/')
def index():
    return 'Hello, Boss! I am THE PIRATES-AI'


@app.route('/invite', methods=['POST'])
def invite():

    session_id = ApiInviteRequest.get_session_id(request)
    token_id = ApiInviteRequest.get_token_id(request)
    print request.json
    board_width = ApiInviteRequest.get_board_width(request)
    board_height = ApiInviteRequest.get_board_height(request)
    ships = ApiInviteRequest.get_ships(request)

    board = Board(board_width, board_height)

    # store init MAP_STATUS with all zeros
    map_status = [[0] * board_height for i in range(board_width)]
    remain_ships = FireHelper.init_remain_ships(ships)

    map_probability = FireHelper.create_probability_map(map_status, remain_ships, board_width, board_height)

    ai_queue = deque()
    hit_points = []

    CacheHelper.cache_info(db, CacheHelper.get_board_key(session_id), board)
    CacheHelper.cache_info(db, CacheHelper.get_map_status_key(session_id), map_status)
    CacheHelper.cache_info(db, CacheHelper.get_queue_key(session_id), ai_queue)
    CacheHelper.cache_info(db, CacheHelper.get_hit_points_key(session_id), hit_points)
    CacheHelper.cache_info(db, CacheHelper.get_ship_remain_key(session_id), remain_ships)
    CacheHelper.cache_info(db, CacheHelper.get_map_prob_key(session_id), map_probability)

    # store ship's information to cache for working in the next steps
    CacheHelper.cache_info(db, CacheHelper.get_ship_info_key(session_id), ships)

    return ApiResponse.response_to_invitation(session_id, token_id)


@app.route('/place-ships', methods=['POST'])
def start():
    session_id = ApiPlaceShipsRequest.get_session_id(request)
    token_id = ApiPlaceShipsRequest.get_token_id(request)

    print request.json

    player_1 = ApiPlaceShipsRequest.get_id_player1(request)
    player_2 = ApiPlaceShipsRequest.get_id_player2(request)

    competitor = player_1
    if player_1 == GameConfig.PLAYER_ID:
        competitor = player_2

    # store competitor id
    CacheHelper.cache_info(db, CacheHelper.get_competitor_id_key(session_id), competitor)

    # history hit for this player
    current_hit = CacheHelper.get_cache(db, CacheHelper.get_history_hit_key(competitor)) or []

    # prioritize hit for this player
    player_setting = PLAYER_MAP.get(competitor) or PLAYER_MAP.get('default')
    prioritize_shots = player_setting.get('prioritize-shot') or []
    CacheHelper.cache_info(db, CacheHelper.get_prioritize_shots_key(session_id), prioritize_shots)

    print 'History hit of {} is : {}'.format(competitor, ', '.join([str(head) for head in current_hit]))

    # reset history hit for this player
    CacheHelper.cache_info(db, CacheHelper.get_history_hit_key(competitor), [])

    # store history hit for current shot
    CacheHelper.cache_info(db, CacheHelper.get_history_hit_key(session_id), current_hit)

    # get ships information from cache to do strategy
    ship_info_arr = CacheHelper.get_cache(db, CacheHelper.get_ship_info_key(session_id))
    board = CacheHelper.get_cache(db, CacheHelper.get_board_key(session_id))
    # init board: place ships
    board.init_board(ship_info_arr, competitor)
    # preview
    board.preview_placed_ships()
    placed_ships = board.get_placed_ships_to_response()

    # store board information
    CacheHelper.cache_info(db, CacheHelper.get_board_key(session_id), board)

    # store match information
    data_collector.store_match_infos(session_id, competitor)

    return ApiResponse.response_to_place_ship(placed_ships, session_id, token_id)


@app.route('/shoot', methods=['POST'])
def turn():
    session_id = ApiShootRequest.get_session_id(request)
    token_id = ApiShootRequest.get_token_id(request)
    max_shots = ApiShootRequest.get_max_shots(request)

    print request.json

    # history hit for this player
    history_hit = CacheHelper.get_cache(db, CacheHelper.get_history_hit_key(session_id))
    prioritize_shots = CacheHelper.get_cache(db, CacheHelper.get_prioritize_shots_key(session_id))

    hit_points = CacheHelper.get_cache(db, CacheHelper.get_hit_points_key(session_id))
    board = CacheHelper.get_cache(db, CacheHelper.get_board_key(session_id))
    map_status = CacheHelper.get_cache(db, CacheHelper.get_map_status_key(session_id))

    map_probability = CacheHelper.get_cache(db, CacheHelper.get_map_prob_key(session_id))
    remain_ships = CacheHelper.get_cache(db, CacheHelper.get_ship_remain_key(session_id))

    points, history_hit, prioritize_shots = FireLogic.fire(remain_ships, map_status, hit_points, map_probability,
                                                           board.width, board.height, history_hit,
                                                           prioritize_shots, max_shots)
    CacheHelper.cache_info(db, CacheHelper.get_history_hit_key(session_id), history_hit)
    CacheHelper.cache_info(db, CacheHelper.get_prioritize_shots_key(session_id), prioritize_shots)

    return ApiResponse.response_to_shoot(points, session_id, token_id)


@app.route('/notify', methods=['POST'])
def notify():
    session_id = ApiNotifyRequest.get_session_id(request)
    token_id = ApiNotifyRequest.get_token_id(request)

    print request.json

    player_id = ApiNotifyRequest.get_player_id(request)
    shots = ApiNotifyRequest.get_shots(request)
    sunk_ships = ApiNotifyRequest.get_sunk_ships(request)

    # get data from cache
    board = CacheHelper.get_cache(db, CacheHelper.get_board_key(session_id))
    map_status = CacheHelper.get_cache(db, CacheHelper.get_map_status_key(session_id))
    map_probability = CacheHelper.get_cache(db, CacheHelper.get_map_prob_key(session_id))
    hit_points = CacheHelper.get_cache(db, CacheHelper.get_hit_points_key(session_id))
    remain_ships = CacheHelper.get_cache(db, CacheHelper.get_ship_remain_key(session_id))
    # get competitor id
    competitor = CacheHelper.get_cache(db, CacheHelper.get_competitor_id_key(session_id))

    # history hit for current session
    current_hit = CacheHelper.get_cache(db, CacheHelper.get_history_hit_key(competitor)) or []

    if player_id == GameConfig.PLAYER_ID:
        for shot in shots:
            x, y, status = shot['coordinate'][0], shot['coordinate'][1], shot['status']
            map_probability[x][y] = 0
            if status == GameConfig.HIT:
                map_status[x][y] = AiConfig.MAP_STATUS_HIT
                hit_points.append(Point(x, y))
            elif status == GameConfig.MISS:
                map_status[x][y] = AiConfig.MAP_STATUS_MISS
                map_probability = FireHelper.create_probability_map(map_status, remain_ships, board.width, board.height)

        # clear sunk ship points in hit points
        if sunk_ships:
            for sunk_ship in sunk_ships:
                # add ship head to current history hit
                head = sunk_ship.get('coordinates')[0]
                current_hit.append(Point(head[0], head[1]))
                hit_points = FireHelper.clear_sunk_ship_points(hit_points, sunk_ship)
                remain_ships = FireHelper.update_remain_ships(sunk_ship, remain_ships)
                print 'Remain sunk_ship types: {}'.format(', '.join([ship.type for ship in remain_ships]))

            map_probability = FireHelper.create_probability_map(map_status, remain_ships, board.width, board.height)
            CacheHelper.cache_info(db, CacheHelper.get_ship_remain_key(session_id), remain_ships)

            # store current history hit to cache
            CacheHelper.cache_info(db, CacheHelper.get_history_hit_key(competitor), current_hit)

    CacheHelper.cache_info(db, CacheHelper.get_map_status_key(session_id), map_status)
    CacheHelper.cache_info(db, CacheHelper.get_map_prob_key(session_id), map_probability)
    CacheHelper.cache_info(db, CacheHelper.get_hit_points_key(session_id), hit_points)

    if GameConfig.PLAYER_ID == player_id and sunk_ships:

        data_collector.store_competitor_ships(session_id, competitor, sunk_ships)

    if GameConfig.PLAYER_ID != player_id:
        data_collector.store_competitor_shoots(session_id, player_id, shots)

    return ApiResponse.response_to_notification(session_id, token_id)


@app.route('/game-over', methods=['POST'])
def game_over():
    session_id = ApiRequest.get_session_id(request)
    token_id = ApiRequest.get_token_id(request)

    return ApiResponse.response_to_notification(session_id, token_id)


if __name__ == '__main__':
    app.run(host=AppConfig.app_host, port=AppConfig.app_port, debug=AppConfig.app_debug)
