import traceback
import uuid
from requests import HTTPError
import requests
import json
from flask import current_app
from util.sb_interfacer import SB_Interfacer
from food.mg_interface import Mongo
from media.bucket_interface import BucketInterface

class SpringBoot(SB_Interfacer):
    # CRUD operations for food
    def __init__(self):
        super().__init__()

    def get_explore_foods_by_cuisine(self, amount_per_category=10):
        data = {"amount": amount_per_category, "group_by": "category.cuisine"}
        try:
            resp = self.__send_request("get_explore_food", "GET", data)["data"]            
        except Exception as e:
            print(str(e))
            raise HTTPError("SB_CONNECTION_FAILED")
        cuisines = set()
        for c in resp:
            cuisines.add(c["_id"])
        return list(cuisines), resp

    def get_explore_foods_by_type(self, amount_per_category=10):
        data = {"amount": amount_per_category, "group_by": "category.type"}
        try:
            resp = self.__send_request("get_explore_food", "GET", data)["data"]
        except Exception as e:
            print(str(e))
            raise HTTPError("SB_CONNECTION_FAILED")
        types = set()
        for c in resp:
            types.add(c["_id"])
        return list(types), resp

    def get_explore_foods_by_perk(self, amount_per_category=10):
        data = {"amount": amount_per_category, "group_by": "category.perks"}
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
            resp = self.__send_request(
                "get_ingredients_option", "GET", {"id_food": food_id}
            )
        except json.JSONDecodeError as e:
            raise HTTPError("FOOD_NOT_FOUND")
        except Exception as e:
            print(str(e))
            raise HTTPError("SB_CONNECTION_FAILED")
        return resp

    def get_food_and_reviews(self, food_id: str) -> dict:
        food = {}
        try:
            food = self.__send_request(
                "get_by_food_id", "GET", {"foodId": food_id}, object="foodreview"
            )
        except Exception as e:
            print(str(e))
            raise Exception("SB_CONNECTION_FAILED")
        
        if "id_food" in food:
            with Mongo() as mg:
                chef = mg.find_chef_by_food(food["id_food"])
                food["chef"] = chef
        return food

    def add_food(self, chef_id: str, food: dict) -> None:
        try:
            food["id_food"] = "food_" + uuid.uuid4().hex
            self.__send_request("add", "POST", food)
            with Mongo() as mg:
                mg.append_food_to_chef(chef_id, food["id_food"])
        except Exception as e:
            print(str(e))
            raise HTTPError("SB_CONNECTION_FAILED")
        return food["id_food"]

    def delete_food(self, chef_id: str, food_id: str) -> None:
        try:
            self.__send_request("DeleteFood", "DELETE", {"id_food": food_id})
            with Mongo() as mg:
                mg.remove_food_from_chef(chef_id, food_id)
        except Exception as e:
            print(str(e))
            raise HTTPError("SB_CONNECTION_FAILED")

    def add_food_review(self, user_id: str, review: dict, role: str) -> None:
        try:
            body = review
            body["id_user"] = user_id
            endpoint = None
            if role == "customer":
                endpoint = "Addreview"
            else:
                endpoint = "AddreviewChef"
            code, resp = self.__send_request(endpoint, "POST", body, object="foodreview", incl_code=True)
        except Exception as e:
            print(str(e))
            raise HTTPError("SB_CONNECTION_FAILED")
        if code != 200:
                raise Exception(resp["error"])

    def __send_dummy_request(self, url, method, body=None):
        if body:
            payload = json.dumps(body)
        else:
            payload = None
        headers = {"Content-Type": "application/json"}
        response = requests.request(method, url, headers=headers, data=payload)
        resp = response.text
        return json.loads(resp)

    def __send_request(self, endpoint, method, body, object="food", incl_code=False):
        url = self._get_url(object, endpoint)
        payload = json.dumps(body)
        headers = {"Content-Type": "application/json"}
        response = requests.request(method, url, headers=headers, data=payload)
        resp = response.text
        print(resp)  ## TODO Remove this line
        if incl_code:
            return response.status_code, json.loads(resp)
        return json.loads(resp)
