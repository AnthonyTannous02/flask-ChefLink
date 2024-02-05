from auth import bp
from flask import request
import flask, time, datetime
from auth.firebase import Firebase
from auth.sb_interface import SpringBoot as sb

@bp.route("/register", methods=["POST"])
def register():
    email = request.json['email']
    password = request.json['password']
    phone_nb = request.json['phone_nb']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    username = request.json['username']
    pp_url = request.json['pp_url']
    print("hi")
    
    return {"data": "x"}


@bp.route("/login", methods=["POST"])           ## TODO include Phone Number & SMS verification
def login():
    username = request.json['username']
    # phone_nb = request.json['phone_nb']
    password = request.json['password']
    
    email = sb.get_email(username)
    
    with Firebase() as fb:
        uid = fb.sign_in(email, password)
        if uid:
            return "hello"
    return "bye"
    
    
