import json
import requests
from util.context_manager import ContextManager
from flask import current_app


class SB_Interfacer(ContextManager):
    def __init__(self):
        super().__init__()
        self.__sb_url = current_app.config["SPRING_BOOT_URL"]

    def _get_attrib_user(        ## TODO Make compatible to both Customers and Chefs
        self,
        id_type,
        value,
        attribs=[
            "uUID",
            "username",
            "email",
            "phone_Number",
            "gender",
            "firstName",
            "lastName",
            "dateOfBirth",
            "p_URL",
        ],
    ) -> dict:
        url = self._get_url("Customer", "GetAttrib")
        payload = json.dumps({"attribs": attribs, "id_type": id_type, "value": value})
        headers = {"Content-Type": "application/json"}
        resp = requests.request("GET", url, headers=headers, data=payload)
        resp = resp.text
        return json.loads(resp)

    def _get_url(self, table, endpoint):
        url = self.__sb_url + "/api/"
        if table == "":
            return url + endpoint
        return url + table + "/" + endpoint

    def __exit__(self, exc_type, exc_value, tb):
        del self.__sb_url
        super().__exit__(exc_type, exc_value, tb)
