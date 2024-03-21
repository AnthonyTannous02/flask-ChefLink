from util.mg_interfacer import MG_Interfacer
from flask_pymongo.wrappers import Database
from flask import current_app


class Mongo(MG_Interfacer):
    def __init__(self):
        super().__init__()

    def get_bookmarks(self, user_id):
        try:
            bookmarks = list(self.__get_conn().Customer.find(
                {"uUID": user_id}, {"bookmarks": 1}
            ))[0]["bookmarks"]
        except:
            raise Exception("DB_CONNECTION_FAILED")
        return bookmarks

    def __get_conn(self) -> Database:
        return self._conn
