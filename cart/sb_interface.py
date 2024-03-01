import json, requests
from flask_jwt_extended import current_app

class SpringBoot():
    @staticmethod
    def get_active_cart(uUID):
        data = {
            "uUID": uUID,
            "status": "A"
        }
        # resp = SpringBoot.__send_request("get_active_cart", "GET", data)             ## TODO Replace with this line


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