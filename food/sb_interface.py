from requests import HTTPError
import requests
import json
from flask import current_app


class SpringBoot:
    # CRUD operations for food
    @staticmethod
    def get_explore_foods_by_cuisine(
        amount_per_category=10,
    ):
        data = {
            "amount": amount_per_category,
            "group_by": "cuisine",
            "attribs": [
                "name",
                "price",
                "picture",
                "cuisine",
                "total_rating",
                "time_till_completion",
            ],
        }
        # resp = SpringBoot.__send_request("get_explore_food", "GET", data)             ## TODO Replace with this line
        resp = SpringBoot.__send_dummy_request(
            "http://127.0.0.1:3030/get", "GET"
        )  ## TODO Remove this line
        cuisines = resp.keys()
        return cuisines, resp

    @staticmethod
    def get_explore_foods_by_perk(
        amount_per_category=5,
    ):
        data = {
            "amount": amount_per_category,
            "group_by": "perk",
            "attribs": [
                "name",
                "price",
                "picture",
                "cuisine",
                "total_rating",
                "time_till_completion",
            ],
        }
        # resp = SpringBoot.__send_request("get_explore_food", "GET", data)             ## TODO Replace with this line
        resp = SpringBoot.__send_dummy_request(
            "http://127.0.0.1:3030/get2", "GET"
        )  ## TODO Remove this line
        perks = resp.keys()
        return perks, resp

    @staticmethod
    def __send_dummy_request(url, method, body=None):
        if body:
            payload = json.dumps(body)
        else:
            payload = None
        headers = {"Content-Type": "application/json"}
        response = requests.request(method, url, headers=headers, data=payload)
        resp = response.text
        return json.loads(resp)

    @staticmethod
    def __send_request(endpoint, method, body):
        url = SpringBoot.__get_url("food", endpoint)
        payload = json.dumps(body)
        headers = {"Content-Type": "application/json"}
        response = requests.request(method, url, headers=headers, data=payload)
        resp = response.text
        return json.loads(resp)

    @staticmethod
    def __get_url(table, endpoint):
        return (
            str(current_app.config["SPRING_BOOT_URL"])
            + "/api/"
            + table
            + "/"
            + endpoint
        )
