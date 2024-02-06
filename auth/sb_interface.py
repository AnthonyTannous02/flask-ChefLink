from requests import HTTPError
import requests
import json
from flask import config

class SpringBoot():
    @staticmethod
    def get_url(table, resource):
        return config["SPRING_BOOT_URL"] + "/api/" + table + "/" + resource
    
    @staticmethod
    def get_email(value, attribute): ## TODO
        email = ""
        url = SpringBoot.get_url("Customer", "GetEmail")
        payload = json.dumps({attribute: value})
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)        
        return email
    
    @staticmethod
    def add_user(uid, email, phone_nb, first_name, last_name, username, pp_url, gender, dob):
        url = SpringBoot.get_url("Customer", "Add")
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