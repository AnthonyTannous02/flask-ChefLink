import uuid
from util.mg_interfacer import MG_Interfacer
from flask_pymongo.wrappers import Database
from flask import current_app


class Mongo(MG_Interfacer):
    def __init__(self):
        super().__init__()

    def get_locations(self, loc_ids: list) -> list:
        locs = []
        try:
            locs = list(self._conn.Location.find({"id_location": {"$in": loc_ids}}, {"_id": 0}))
        except Exception as e:
            print(str(e))
            raise("DB_CONNECTION_FAILED")
        return locs

    def get_location_by_id(self, loc_id: str, role: str) -> dict:
        loc_in_user = {}
        loc = {}
        
        try:
            if role == "customer":
                loc_in_user = self._conn.Customer.find_one({"locations": loc_id}, {"_id": 0})
            else:
                loc_in_user = self._conn.Chef.find_one({"locations": loc_id}, {"_id": 0})
            loc = self._conn.Location.find_one({"id_location": loc_id}, {"_id": 0})
        except Exception as e:
            print(str(e))
            raise Exception("DB_CONNECTION_FAILED")
        
        if loc_in_user is None or loc is None:
            raise Exception("LOCATION_NOT_FOUND")
        return loc

    def add_location(self, user_id: str, location: dict, role: str) -> None:
        keys = [
            "location_name",
            "longitude",
            "latitude",
            "phone_number",
            "street",
            "building",
            "apartment",
            "instructions",
        ]
        if not all(key in location for key in keys):
            raise Exception("INVALID_LOCATION_DATA")
        
        try:
            location["id_location"] = "loc_" + uuid.uuid4().hex
            self._conn.Location.insert_one(location)
            if role == "customer":
                self._conn.Customer.update_one(
                    {"uUID": user_id},
                    {"$push": {"locations": location["id_location"]}}
                )
            else:
                self._conn.Chef.update_one(
                    {"uUID": user_id},
                    {"$push": {"locations": location["id_location"]}}
                )
        except Exception as e:
            print(str(e))
            raise Exception("DB_CONNECTION_FAILED")

    def remove_location(self, user_id: str, loc_id: str, role: str) -> None:
        res = self._conn.Location.find_one_and_delete({"id_location": loc_id})
        if not res or len(res) < 1:
            raise Exception("LOCATION_NOT_FOUND")
        if role == "customer":
            self._conn.Customer.update_one(
                {"uUID": user_id},
                {
                    "$pull": {"locations": loc_id},
                }
            )
        else:
            self._conn.Chef.update_one(
                {"uUID": user_id},
                {
                    "$pull": {"locations": loc_id},
                }
            )
