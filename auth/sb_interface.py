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

    # def get_email(self, id_type, value):
    #     get_attrib_resp = self.__get_attrib(id_type, value, ["email"])
    #     if "email" in get_attrib_resp:
    #         return get_attrib_resp["email"]
    #     else:
    #         raise HTTPError("WRONG_UN_PW")

    def add_user(
        self, fb, email, phone_nb, first_name, last_name, username, pp_url, gender, dob, password, role
    ):
        uid = fb.sign_up(email, password, role)
        if role == "customer":
            url = self._get_url("Customer", "AddC")
            method = "PUT"
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
        else:
            url = self._get_url("", "AddChef")
            method = "POST"
            payload = json.dumps({
                    "username": username,
                    "uUID": uid,
                    "email": email,
                    "phone_Number": phone_nb,
                    "gender": gender,
                    "firstName": first_name,
                    "lastName": last_name,
                    "foodList": [],
                    "dateOfBirth": dob,
                    "bookmarks": [],
                    "p_URL": pp_url,
                    "locations": [],
                    "_class": "com.SoftwareEngineeringProject.demo.entity.Chef"
                }
            )
        
        headers = {"Content-Type": "application/json"}
        resp = requests.request(method, url, headers=headers, data=payload)
        print(resp)
        if resp.status_code != 200:
            raise Exception("SB_CONNECTION_FAILED")

    def get_email_jwt_claims(self, id_type, value):
        get_attrib_resp = self.__get_attrib(
            id_type, value, ["email", "username", "p_URL"]
        )
        if ("username" in get_attrib_resp and "p_URL" in get_attrib_resp and "email" in get_attrib_resp):
            return (
                get_attrib_resp["email"],
                get_attrib_resp["username"],
                get_attrib_resp["p_URL"],
            )
        else:
            raise HTTPError("WRONG_CREDENTIALS")

    def add_rem_bookmarks(self, user_id, food_id, role):
        if role == "customer":
            url = self._get_url("", "addBookmark")
        else:
            url = self._get_url("", "addBookmarkChef")
        payload = json.dumps({"uUID": user_id, "id_food": food_id})
        headers = {"Content-Type": "application/json"}
        resp = json.loads(requests.request("PUT", url, headers=headers, data=payload).text)
        print(resp)
        if "status" in resp and (resp["status"] == "successful" or resp["status"] == "SUCCESS"):
            return str(resp["bookmark"]).upper()
        else:
            if "user" in resp["description"]:
                raise HTTPError("USER_NOT_FOUND")
            if "food" in resp["description"]:
                raise HTTPError("FOOD_NOT_FOUND")
            raise HTTPError(resp["description"])

    def get_bookmarks(self, user_id, role):
        if role == "customer":
            url = self._get_url("", "getBookMarkedFoodId")
        else:
            url = self._get_url("", "getBookMarkedFoodIdChef")
        payload = json.dumps({"uUID": user_id})
        headers = {"Content-Type": "application/json"}
        resp:dict = json.loads(requests.request("GET", url, headers=headers, data=payload).text)
        resp.pop("uUID", None)
        print(resp)
        return resp

    def get_profile_page_info(self, user_id, role):
        attribs = ["uUID", "username", "email", "phone_Number", "gender", "firstName", "lastName", "dateOfBirth"]
        if role == "customer":
            url = self._get_url("Customer", "GetAttrib")
        else:
            url = self._get_url("Chef", "GetAttrib")
        payload = json.dumps({"attribs": attribs, "id_type": "uUID", "value": user_id})
        headers = {"Content-Type": "application/json"}
        resp = requests.request("GET", url, headers=headers, data=payload)
        return json.loads(resp.text)

    def update_profile(self, user_id, attribs_to_change, attribs_new_vals, role) -> dict:
        if role == "customer":
            url = self._get_url("", "UpdateInfo")
        else:
            url = self._get_url("", "UpdateInfoChef")
        payload = json.dumps(
            {
                "uUID": user_id,
                "To Change": attribs_to_change,
                "New Values": attribs_new_vals,
            }
        )
        headers = {"Content-Type": "application/json"}
        resp = requests.request("PUT", url, headers=headers, data=payload)
        return json.loads(resp.text)

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
        url1 = self._get_url("Customer", "GetAttrib")
        url2 = self._get_url("Chef", "GetAttrib")
        payload = json.dumps({"attribs": attribs, "id_type": id_type, "value": value})
        headers = {"Content-Type": "application/json"}
        resp1 = requests.request("GET", url1, headers=headers, data=payload)
        resp2 = requests.request("GET", url2, headers=headers, data=payload)
        resp = resp2.text if "error" in resp1.text else resp1.text
        return json.loads(resp)
