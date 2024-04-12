import uuid
from util.mg_interfacer import MG_Interfacer
from flask_pymongo.wrappers import Database


class Mongo(MG_Interfacer):
    def __init__(self):
        super().__init__()
    
    def check_for_dups(self, username, phone_nb):
        self._conn.Customer.dis
        user = self._conn.Customer.find_one({"username": username})
        if user:
            raise Exception("USERNAME_EXISTS")
        user = self._conn.Customer.find_one({"phone_Number": phone_nb})
        if user:
            raise Exception("PHONE_NB_EXISTS")