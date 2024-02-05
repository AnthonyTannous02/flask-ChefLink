import json
import traceback
import pyrebase
import requests

class Firebase():
    def __init__(self):
        config={
            "apiKey": "AIzaSyC8EJP1OlmChtZwGslv-Yt0A2APZn1pGrw",
            "authDomain": "cheflink-42508.firebaseapp.com",
            "projectId": "cheflink-42508",
            "databaseURL": "",
            "storageBucket": "cheflink-42508.appspot.com",
            "messagingSenderId": "985394133585",
            "appId": "1:985394133585:web:7e71ce339082b6639b5670",
            "measurementId": "G-Q1CQJJT48Z"
        }
        self.pyrebase = pyrebase.initialize_app(config)
        self.auth = self.pyrebase.auth()
        
    def sign_up(self, email, password):
        user = self.auth.create_user_with_email_and_password(email=email, password=password)
        # self.auth.send_email_verification(user['idToken'])
        return user.get('localId')
    
    def sign_in(self, email, password):
        user = self.auth.sign_in_with_email_and_password(email, password)
        # email_ver = self.auth.get_account_info(user['idToken'])['users'][0]['emailVerified']
        # if email_ver:
        # print(user)
        return user.get('localId')
        # return
    
    # def send_pw_reset_mail(self, email):
    #     status = self.auth.send_password_reset_email(email)
    #     return status
    
    # def change_password(self, code, password):
    #     return self.auth.verify_password_reset_code(code, password) 
    
    # def verify_email(self, code):
    #     request_ref = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={self.pyrebase.api_key}"
    #     headers = {"content-type": "application/json; charset=UTF-8"}
    #     data = json.dumps({"oobCode": code})
    #     obj = requests.post(request_ref, headers=headers, data=data)
    #     Firebase.raise_err(obj)
    #     return obj.json()
    
    # def verify_pw_code(self, code):
    #     request_ref = f"https://identitytoolkit.googleapis.com/v1/accounts:resetPassword?key={self.pyrebase.api_key}"
    #     headers = {"content-type": "application/json; charset=UTF-8"}
    #     data = json.dumps({"oobCode": code})
    #     obj = requests.post(request_ref, headers=headers, data=data)
    #     Firebase.raise_err(obj)
    #     return obj.json()
    
    # def del_user(self, email, password):
    #     self.auth.delete_user_account(self.auth.sign_in_with_email_and_password(email, password)['idToken'])
    
    @staticmethod
    def raise_err(request_object):
        try:
            request_object.raise_for_status()
        except requests.HTTPError as e:
            raise requests.HTTPError(e, request_object.text)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
        
        del self.auth, self.pyrebase, self
        return True