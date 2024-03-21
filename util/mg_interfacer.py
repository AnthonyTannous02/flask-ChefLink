from util.interfacer import Interfacer
from flask import current_app
from flask_pymongo.wrappers import Database

class MG_Interfacer(Interfacer):
    def __init__(self):
        super().__init__()
        self._conn:Database = current_app.config["mongo"].get_database("ChefLink")

    def __exit__(self, exc_type, exc_value, tb):
        del self._conn
        super().__exit__(exc_type, exc_value, tb)