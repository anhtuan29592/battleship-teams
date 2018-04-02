from flask import jsonify, make_response


class ApiRequest(object):
    @staticmethod
    def get_session_id(request):
        return request.headers.get('X-SESSION-ID')

    @staticmethod
    def get_token_id(request):
        return request.headers.get('X-TOKEN')


class ApiInviteRequest(ApiRequest):
    @staticmethod
    def get_board_width(request):
        """

        :param request:
        :return: MAX_OF_X
        """
        return request.json.get('boardWidth')

    @staticmethod
    def get_board_height(request):
        """

        :param request:
        :return: MAX_OF_Y
        """
        return request.json.get('boardHeight')

    @staticmethod
    def get_ships(request):
        return request.json.get('ships')


class ApiPlaceShipsRequest(ApiRequest):
    @staticmethod
    def get_id_player1(request):
        return request.json.get('player1')

    @staticmethod
    def get_id_player2(request):
        return request.json.get('player2')


class ApiShootRequest(ApiRequest):
    @staticmethod
    def get_max_shots(request):
        return request.json.get('maxShots')


class ApiNotifyRequest(ApiRequest):
    @staticmethod
    def get_player_id(request):
        return request.json.get('playerId')

    @staticmethod
    def get_shots(request):
        return request.json.get('shots')

    @staticmethod
    def get_sunk_ships(request):
        return request.json.get('sunkShips')


class ApiResponse(object):
    @staticmethod
    def create_response_with_header(data, session_id, token_id):
        res = make_response(data)
        res.headers['X-SESSION-ID'] = session_id
        res.headers['X-TOKEN'] = token_id

        return res

    @staticmethod
    def response_to_invitation(session_id, token_id):
        data = jsonify(
            {
                'success': True
            }
        )

        return ApiResponse.create_response_with_header(data, session_id, token_id)

    @staticmethod
    def response_to_place_ship(ships, session_id, token_id):
        data = jsonify(
            {
                'ships': ships
            }
        )

        return ApiResponse.create_response_with_header(data, session_id, token_id)

    @staticmethod
    def response_to_shoot(points, session_id, token_id):
        data = jsonify(
            {
                'coordinates': points
            }
        )

        return ApiResponse.create_response_with_header(data, session_id, token_id)

    @staticmethod
    def response_to_notification(session_id, token_id):
        data = jsonify(
            {
                'success': True
            }
        )

        return ApiResponse.create_response_with_header(data, session_id, token_id)

    @staticmethod
    def response_to_game_over(session_id, token_id):
        data = jsonify(
            {
                'success': True
            }
        )

        return ApiResponse.create_response_with_header(data, session_id, token_id)