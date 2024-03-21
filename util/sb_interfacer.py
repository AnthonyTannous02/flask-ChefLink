from util.interfacer import Interfacer
from flask import current_app


class SB_Interfacer(Interfacer):
    def __init__(self):
        super().__init__()
        self.__sb_url = current_app.config["SPRING_BOOT_URL"]

    def _get_url(self, table, endpoint):
        url = self.__sb_url + "/api/"
        if table == "":
            return url + endpoint
        return url + table + "/" + endpoint

    def __exit__(self, exc_type, exc_value, tb):
        del self.__sb_url
        super().__exit__(exc_type, exc_value, tb)
