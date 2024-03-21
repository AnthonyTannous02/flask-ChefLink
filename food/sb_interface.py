import traceback
from requests import HTTPError
import requests
import json
from flask import current_app
from util.sb_interfacer import SB_Interfacer

class SpringBoot(SB_Interfacer):
    # CRUD operations for food
    def __init__(self):
        super().__init__()

    def get_explore_foods_by_cuisine(self, amount_per_category=10):
        data = {
            "amount": amount_per_category,
            "group_by": "category.cuisine"
        }
        try:
            resp = self.__send_request("get_explore_food", "GET", data)["data"]
        except Exception as e:
            print(str(e))
            raise HTTPError("SB_CONNECTION_FAILED")
        cuisines = set()
        for c in resp:
            cuisines.add(c["_id"])
        return list(cuisines), resp

    def get_explore_foods_by_perk(self, amount_per_category=10):
        data = {
            "amount": amount_per_category,
            "group_by": "category.perks"
        }
        try:
            resp = self.__send_request("get_explore_food", "GET", data)["data"]
        except Exception as e:
            print(str(e))
            raise HTTPError("SB_CONNECTION_FAILED")
        perks = set()
        for food in resp:
            for perk in food["_id"]:
                perks.add(perk)
        
        return list(perks), resp

    def get_ingred_options(self, food_id):
        try:
            resp = self.__send_request("get_ingredients_option", "GET", {"id_food": food_id})
        except json.JSONDecodeError as e:
            raise HTTPError("FOOD_NOT_FOUND")
        except Exception as e:
            print(str(e))
            raise HTTPError("SB_CONNECTION_FAILED")
        return resp

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
        print(resp) ## TODO Remove this line
        return json.loads(resp)