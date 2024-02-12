from auth import bp
from flask import jsonify, request
from auth.firebase import Firebase
from auth.sb_interface import SpringBoot as sb
from flask_jwt_extended import (
        create_access_token, create_refresh_token, jwt_required,
        set_access_cookies, set_refresh_cookies, unset_jwt_cookies,
        current_user, get_jwt_identity,
    )


@bp.route("/register", methods=["PUT"])
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
    
    if(not phone_nb[1:].isdigit() or phone_nb[0] != "+"):
        return {"status": "FAIL", "error": "INVALID_REQUEST"}, 400
    
    with Firebase() as fb:
        try:
            uid = fb.sign_up(email, password)
            if uid:
                sc = sb.add_user(uid, email, phone_nb, first_name, last_name, username, pp_url, gender, date_of_birth)
                print(sc)
                if sc == 201:
                    return {"status": "SUCCESS"}, 200
            return {"status": "FAIL", "error": "INVALID_CREDENTIALS"}, 400
        except Exception as e:
            return {"status": "FAIL", "error": str(e)}, 400


@bp.route("/login", methods=["POST"])           ## TODO include Phone Number & SMS verification
def login():
    if request.cookies.get("access_token_cookie"):
        return {"status": "FAIL", "error": "ALREADY_LOGGED_IN"}, 400
    
    try:    
        password = request.json['password']
        if "username" in request.json:
            username = request.json['username']
            email = sb.get_email("username", username)
        elif "phone_nb" in request.json:
            phone_nb = request.json['phone_nb']
            email = sb.get_email("phone_Number", phone_nb)
        else:
            return {"status": "FAIL", "error": "INVALID_REQUEST"}, 400
        
        with Firebase() as fb:
            id = fb.sign_in(email, password)
            if id:
                access_token =  create_access_token(identity=id)
                refresh_token =  create_refresh_token(identity=id)
                resp = jsonify({"status": "SUCCESS"})
                set_access_cookies(resp, access_token)
                set_refresh_cookies(resp, refresh_token)
                return resp, 200
        return {"status": "FAIL", "error": "WRONG_UN_PW"}, 400
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400


@bp.route("/refresh", methods=["GET"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    resp = jsonify({"status": "SUCCESS"})
    set_access_cookies(resp, access_token)
    return resp, 200


@bp.route("/logout")
def logout():
    if not request.cookies.get("access_token_cookie"):
        return {"status": "FAIL", "error": "NOT_LOGGED_IN"}, 400
    resp = jsonify({"status": "SUCCESS"})
    unset_jwt_cookies(resp)
    return resp, 200


@bp.route("/")
@jwt_required()
def index():
    return {"test": "Hello, World! I am the auth blueprint from Flask."}