import traceback, pyrebase, requests, os
from firebase_admin import auth

class Firebase():
    def __init__(self):
        config = {
            "apiKey": os.getenv("FIREBASE_API_KEY"),
            "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
            "projectId": os.getenv("FIREBASE_PROJECT_ID"),
            "databaseURL": "",
            "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
            "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
            "appId": os.getenv("FIREBASE_APP_ID"),
            "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID")
        }
        self.pyrebase = pyrebase.initialize_app(config)
        self.auth = self.pyrebase.auth()
        
    def sign_up(self, email, password, role):
        user = self.auth.create_user_with_email_and_password(email=email, password=password)
        auth.set_custom_user_claims(user.get('localId'), {'role': role})
        return user.get('localId')
    
    def sign_in(self, email, password):
        user = self.auth.sign_in_with_email_and_password(email, password)
        try:
            role = auth.get_user(user.get('localId')).custom_claims["role"]
        except Exception as e:
            role = "customer"
        print(role)
        return user.get('localId'), role
    
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