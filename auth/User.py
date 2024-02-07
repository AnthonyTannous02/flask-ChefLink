from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, username, phone_nb):
        self.id = id
        self.email = email 
        self.username = username
        self.phone_nb = phone_nb