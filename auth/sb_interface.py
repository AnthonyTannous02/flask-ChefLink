import traceback
from requests import HTTPError
import requests
import json
from flask import current_app
from util.sb_interfacer import SB_Interfacer

class SpringBoot(SB_Interfacer):
    # CRUD operations for auth
    def __init__(self):
        super().__init__()

    def get_email(self, id_type, value):
        get_attrib_resp = self.__get_attrib(id_type, value, ["email"])
        if "email" in get_attrib_resp:
            return get_attrib_resp["email"]
        else:
            raise HTTPError("WRONG_UN_PW")

    def add_user(
        self, uid, email, phone_nb, first_name, last_name, username, pp_url, gender, dob
    ):
        url = self._get_url("Customer", "Add")
        payload = json.dumps(
            {
                "uUID": uid,
                "username": username,
                "email": email,
                "phone_Number": phone_nb,
                "gender": gender,
                "firstName": first_name,
                "lastName": last_name,
                "dateOfBirth": dob,
                "bookmarks": [],
                "p_URL": pp_url,
            }
        )
        headers = {"Content-Type": "application/json"}
        resp = requests.request("PUT", url, headers=headers, data=payload)
        # raise HTTPError("xxx")
        return resp.status_code

    def get_email_jwt_claims(self, id_type, value):
        get_attrib_resp = self.__get_attrib(
            id_type, value, ["email", "username", "p_URL"]
        )
        if (
            "username" in get_attrib_resp
            and "p_URL" in get_attrib_resp
            and "email" in get_attrib_resp
        ):
            return (
                get_attrib_resp["email"],
                get_attrib_resp["username"],
                get_attrib_resp["p_URL"],
            )
        else:
            raise HTTPError("WRONG_CREDENTIALS")

    def add_rem_bookmarks(self, user_id, food_id):
        url = self._get_url("", "addBookmark")
        payload = json.dumps({"uUID": user_id, "id_food": food_id})
        headers = {"Content-Type": "application/json"}
        resp = json.loads(requests.request("PUT", url, headers=headers, data=payload).text)
        print(resp)
        if "success" in resp["status"]:
            return str(resp["bookmark"]).upper()
        else:
            if "user" in resp["description"]:
                raise HTTPError("USER_NOT_FOUND")
            if "food" in resp["description"]:
                raise HTTPError("FOOD_NOT_FOUND")
            raise HTTPError(resp["description"])

    def get_bookmarks(self, user_id):
        url = self._get_url("", "getBookMarkedFoodId")
        payload = json.dumps({"uUID": user_id})
        headers = {"Content-Type": "application/json"}
        resp:dict = json.loads(requests.request("GET", url, headers=headers, data=payload).text)
        resp.pop("uUID", None)
        print(resp)
        return resp

    def test(self, id_type, value):
        resp = self.__get_attrib(id_type, value)
        return resp

    def __get_attrib(
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
    ):
        url = self._get_url("Customer", "GetAttrib")
        payload = json.dumps({"attribs": attribs, "id_type": id_type, "value": value})
        headers = {"Content-Type": "application/json"}
        resp = requests.request("GET", url, headers=headers, data=payload)
        resp = resp.text
        return json.loads(resp)
