from datetime import datetime


class DataCollector(object):

    def __init__(self, mongo_db):
        self.mongo_db = mongo_db

    def store_competitor_ships(self, session_id, player_id, ships):
        self.insert_data('competitor_ships', {
            "session_id": session_id,
            "player_id": player_id,
            "ships": ships,
            "created_time": datetime.now(),
        })

    def store_competitor_shoots(self, session_id, player_id, shots):
        self.insert_data('competitor_shoots', {
            "session_id": session_id,
            "player_id": player_id,
            "shots": shots,
            "created_time": datetime.now(),
        })

    def store_match_infos(self, session_id, competitor):
        self.insert_data('match_infos', {
            "session_id": session_id,
            "competitor": competitor,
            "created_time": datetime.now(),
        })

    def insert_data(self, mongo_collection, data):
        try:
            self.mongo_db[mongo_collection].insert_one(data)
        except Exception as e:
            print(e)
