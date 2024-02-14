from requests import HTTPError
import requests
import json
from flask import current_app
from auth.User import User

class SpringBoot():
    @staticmethod
    def get_email(id_type, value):
        get_attrib_resp = SpringBoot.__get_attrib(id_type, value, ["email"])
        if "email" in get_attrib_resp:
            return get_attrib_resp["email"]
        else:
            raise HTTPError("WRONG_UN_PW")
        
    @staticmethod
    def add_user(uid, email, phone_nb, first_name, last_name, username, pp_url, gender, dob):
        url = SpringBoot.__get_url("Customer", "Add")
        payload = json.dumps({
            "uUID": uid,
            "username": username,
            "email": email,
            "phone_Number": phone_nb,
            "gender": gender,
            "firstName": first_name,
            "lastName": last_name,
            "dateOfBirth": dob,
            "p_URL": pp_url
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.request("PUT", url, headers=headers, data=payload)
        print(response.text)
        # raise HTTPError("xxx")
        return response.status_code
    
    @staticmethod
    def __get_url(table, endpoint):
        return str(current_app.config["SPRING_BOOT_URL"]) + "/api/" + table + "/" + endpoint
    
    @staticmethod
    def __get_attrib(id_type, value, 
                attribs=["uUID", "username", "email", 
                        "phone_Number", "gender", "firstName", 
                        "lastName", "dateOfBirth", "p_URL"]):
        
        url = SpringBoot.__get_url("Customer", "GetAttrib")
        payload = json.dumps({"attribs": attribs, 
                            "id_type": id_type, 
                            "value": value})
        headers = {'Content-Type': 'application/json'}
        response = requests.request("GET", url, headers=headers, data=payload)
        resp = response.text
        print(resp)        
        return json.loads(resp)
    