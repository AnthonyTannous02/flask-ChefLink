from auth import bp
from flask import request
import flask, time, datetime
from auth.firebase import Firebase
from auth.sb_interface import SpringBoot as sb

@bp.route("/register", methods=["POST"])
def register():
    email = request.json['email']
    gender = request.json['gender']
    date_of_birth = request.json['date_of_birth']
    password = request.json['password']
    phone_nb = request.json['phone_nb']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    username = request.json['username']
    pp_url = request.json['pp_url']
    try:
        with Firebase() as fb:
            uid = fb.sign_up(email, password)
            if uid:
                sb.add_user(uid, email, phone_nb, first_name, last_name, username, pp_url, gender, date_of_birth)
                return {"status": "SUCCESS"}, 200
    except Exception as e:
        return {"status": "FAILURE", "error": str(e)}, 400


@bp.route("/login", methods=["POST"])           ## TODO include Phone Number & SMS verification
def login():
    password = request.json['password']
    if "username" in request.json:
        username = request.json['username']
        email = sb.get_email(username, "username")
    elif "phone_nb" in request.json:
        phone_nb = request.json['phone_nb']
        email = sb.get_email(phone_nb, "phone_Number")
    else:
        return {"status": "FAILURE", "error": "Invalid Request"}, 400
    
    with Firebase() as fb:
        uid = fb.sign_in(email, password)
        if uid:
            return "hello"
    return "bye"
    
    
