import cPickle

from settings import CacheConfig


class CacheHelper(object):
    @staticmethod
    def get_board_key(session_id):
        return CacheConfig.BOARD_PREFIX + session_id

    @staticmethod
    def get_history_hit_key(player_id):
        return CacheConfig.HISTORY_HIT_PREFIX + player_id

    @staticmethod
    def get_prioritize_shots_key(session_id):
        return CacheConfig.PRIORITIZE_SHOTS_PREFIX + session_id

    @staticmethod
    def get_map_status_key(session_id):
        return CacheConfig.MAP_STATUS_PREFIX + session_id

    @staticmethod
    def get_competitor_map_key(session_id):
        return CacheConfig.COMPETITOR_MAP_PREFIX + session_id

    @staticmethod
    def get_competitor_id_key(session_id):
        return CacheConfig.COMPETITOR_ID_PREFIX + session_id

    @staticmethod
    def get_ship_info_key(session_id):
        return CacheConfig.SHIP_INFO_PREFIX + session_id

    @staticmethod
    def get_ship_remain_key(session_id):
        return CacheConfig.SHIP_REMAIN_PREFIX + session_id

    @staticmethod
    def get_map_prob_key(session_id):
        return CacheConfig.MAP_PROBABILITY_SUFFIX + session_id

    @staticmethod
    def get_queue_key(session_id):
        return CacheConfig.QUEUE_PREFIX + session_id

    @staticmethod
    def get_hit_points_key(session_id):
        return CacheConfig.HIT_POINTS_PREFIX + session_id

    @staticmethod
    def get_cache(redis, key):
        value = redis.get(key)
        if value:
            return cPickle.loads(value)
        return None

    @staticmethod
    def cache_info(redis, key, value):
        redis.set(key, cPickle.dumps(value))
