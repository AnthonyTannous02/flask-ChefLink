import json, requests
import traceback
from util.sb_interfacer import SB_Interfacer

class SpringBoot(SB_Interfacer):
    # CRUD operations for cart
    def __init__(self):
        super().__init__()

    # def get_stand_by_cart(self, uUID):
    #     data = {
    #         "user_id": uUID,
    #         "status": "Active",
    #         "attribs": [
    #             "cart_id",
    #             "user_id",
    #             "status",
    #         ],
    #     }
    #     # resp = self.__send_request("get_cart", "GET", data)             ## TODO Replace with this line
    #     resp = self.__send_dummy_request("http://127.0.0.1:3030/get_cart1", "GET", data)

    def __send_dummy_request(self, url, method, body=None):
        if body:
            payload = json.dumps(body)
        else:
            payload = None
        headers = {"Content-Type": "application/json"}
        response = requests.request(method, url, headers=headers, data=payload)
        resp = response.text
        return json.loads(resp)

    def __send_request(self, endpoint, method, body):
        url = self._get_url("food", endpoint)
        payload = json.dumps(body)
        headers = {"Content-Type": "application/json"}
        response = requests.request(method, url, headers=headers, data=payload)
        resp = response.text
        return json.loads(resp)
