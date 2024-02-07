from requests import HTTPError
import requests
import json
from flask import config
from auth.User import User

class SpringBoot():
    @staticmethod
    def get_url(table, endpoint):
        return config["SPRING_BOOT_URL"] + "/api/" + table + "/" + endpoint
    
    @staticmethod
    def get_attrib(attribs, id_type, value): ## TODO
        url = SpringBoot.get_url("Customer", "get_attrib")
        payload = json.dumps({"attribs": attribs, 
                            "id_type": id_type, 
                            "value": value})
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)
        resp = response.text
        print(resp)        
        return resp
    
    @staticmethod
    def get_email(id_type, value):
        get_attrib_resp = SpringBoot.get_attrib(["email"], id_type, value)
        if get_attrib_resp:
            email = json.loads(get_attrib_resp)["email"]
            return email
        else:
            raise HTTPError("USER_NOT_FOUND")
    
    @staticmethod
    def add_user(uid, email, phone_nb, first_name, last_name, username, pp_url, gender, dob):
        url = SpringBoot.get_url("Customer", "add")
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
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        # raise HTTPError("xxx")
        return response.status_code == 200