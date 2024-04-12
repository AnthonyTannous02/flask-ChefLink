import requests
import json
from flask import current_app
from util.sb_interfacer import SB_Interfacer


class SpringBoot(SB_Interfacer):
    # CRUD operations for location
    def __init__(self):
        super().__init__()

    def get_loc_ids(self, user_id) -> list:
        loc_ids = self._get_attrib_user("uUID", user_id, ["locations"])
        print(loc_ids)
        return loc_ids["locations"]

    def __send_request(self, endpoint, method, body, object="location"):
        url = self._get_url(object, endpoint)
        payload = json.dumps(body)
        headers = {"Content-Type": "application/json"}
        response = requests.request(method, url, headers=headers, data=payload)
        resp = response.text
        print(resp)  ## TODO Remove this line
        return json.loads(resp)
