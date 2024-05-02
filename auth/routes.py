from auth import bp
from flask import jsonify, request
from auth.firebase import Firebase
from auth.sb_interface import SpringBoot
from auth.mg_interface import Mongo
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
    current_user,
    get_jwt_identity,
    get_jwt,
)


@bp.route("/register", methods=["PUT"])  ## TODO include Phone Number & SMS verification
def register():
    email = request.json["email"]
    gender = request.json["gender"]
    date_of_birth = request.json["date_of_birth"]
    password = request.json["password"]
    phone_nb = request.json["phone_nb"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    username = request.json["username"]
    pp_url = request.json["pp_url"]
    role = request.json["role"]

    if not phone_nb or not phone_nb[1:].isdigit() or phone_nb[0] != "+" or role not in ["customer", "chef"]:
        return {"status": "FAIL", "error": "INVALID_REQUEST"}, 400

    with Firebase() as fb:
        try:
            with Mongo() as mg:
                mg.check_for_dups(username, phone_nb, role)
            with SpringBoot() as sb:
                sb.add_user(
                    fb,
                    email,
                    phone_nb,
                    first_name,
                    last_name,
                    username,
                    pp_url,
                    gender,
                    date_of_birth,
                    password,
                    role,
                )
        except Exception as e:
            if "EMAIL_EXISTS" in str(e):
                return {"status": "FAIL", "error": "EMAIL_EXISTS"}, 400
            elif "WEAK_PASSWORD" in str(e):
                return {"status": "FAIL", "error": "WEAK_PASSWORD"}, 400
            elif "INVALID_EMAIL" in str(e):
                return {"status": "FAIL", "error": "INVALID_EMAIL"}, 400
            return {"status": "FAIL", "error": str(e)}, 400
        return {"status": "SUCCESS"}, 200


@bp.route("/login", methods=["POST"])  ## TODO include Phone Number & SMS verification
def login():
    if request.cookies.get("access_token_cookie"):
        return {"status": "FAIL", "error": "ALREADY_LOGGED_IN"}, 400

    try:
        password = request.json["password"]
        with SpringBoot() as sb:
            if "username" in request.json:
                username = request.json["username"]
                email, username, p_URL = sb.get_email_jwt_claims("username", username)
            elif "phone_nb" in request.json:
                phone_nb = request.json["phone_nb"]
                email, username, p_URL = sb.get_email_jwt_claims(
                    "phone_Number", phone_nb
                )
            else:
                return {"status": "FAIL", "error": "INVALID_REQUEST"}, 400

        with Firebase() as fb:
            id, role = fb.sign_in(email, password)
            if id:                                                       ## TODO: Make it dynamic
                additional_claims = {"username": username, "p_URL": p_URL, "role": role}  ## TODO
                access_token = create_access_token(
                    identity=id, additional_claims=additional_claims
                )
                refresh_token = create_refresh_token(
                    identity=id, additional_claims=additional_claims
                )
                resp = jsonify({"status": "SUCCESS"})
                set_access_cookies(resp, access_token)
                set_refresh_cookies(resp, refresh_token)
                return resp, 200
        return {"status": "FAIL", "error": "WRONG_UN_PW"}, 400
    except Exception as e:
        if "EMAIL_NOT_FOUND" in str(e):
            return {"status": "FAIL", "error": "EMAIL_NOT_FOUND"}, 400
        return {"status": "FAIL", "error": str(e)}, 400


@bp.route("/logout")
def logout():
    if not request.cookies.get("access_token_cookie"):
        return {"status": "FAIL", "error": "NOT_LOGGED_IN"}, 400
    resp = jsonify({"status": "SUCCESS"})
    unset_jwt_cookies(resp)
    return resp, 200


@bp.route("/add_rem_bookmarks", methods=["PUT"])
@jwt_required()
def add_rem_bookmarks():
    try:
        food_id = request.json["food_id"]
        with SpringBoot() as sb:
            resp = sb.add_rem_bookmarks(current_user["uUID"], food_id, current_user["role"])
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400
    return {"status": "SUCCESS", "msg": resp}, 200


@bp.route("/get_bookmarks", methods=["GET"])
@jwt_required()
def get_bookmarks():
    try:
        with SpringBoot() as sb:
            resp = sb.get_bookmarks(current_user["uUID"], current_user["role"])
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400
    return {"status": "SUCCESS", "msg": resp}, 200


@bp.route("/get_profile", methods=["GET"])
@jwt_required(optional=True)
def get_profile():
    claims = get_jwt()
    if not claims or not current_user:
        return {"status": "SUCCESS", "data": ""}, 400
    return {
        "status": "SUCCESS",
        "data": {
            "username": claims["username"],
            "p_URL": claims["p_URL"],
        },
    }, 200


@bp.route("/get_profile_page_info", methods=["GET"])
@jwt_required()
def get_profile_page_info():
    try:
        with SpringBoot() as sb:
            resp = sb.get_profile_page_info(current_user["uUID"], current_user["role"])
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400
    return {"status": "SUCCESS", "data": resp}, 200


@bp.route("/update_profile", methods=["PUT"])
@jwt_required()
def update_profile():
    try:
        attribs_to_change = request.json["attribs_to_change"]
        attribs_new_vals = request.json["attribs_new_vals"]
        with SpringBoot() as sb:
            resp = sb.update_profile(current_user["uUID"], attribs_to_change, attribs_new_vals, current_user["role"])
    except Exception as e:
        return {"status": "FAIL", "error": "INVALID_REQUEST"}, 400
    return {"status": "SUCCESS", "details": resp}, 200

    ## Requests to remove ##


@bp.route("/")
@jwt_required()
def index():
    role = get_jwt()["role"]
    with SpringBoot() as sb:
        resp = sb.test("uUID", current_user["uUID"])
    return {
        "Message": "Hello, " + resp["username"] + ". Welcome to the Auth Blueprint! You are a " + role + "!",
        "uUID": resp["uUID"],
        "username": resp["username"],
        "email": resp["email"],
        "phone_nb": resp["phone_Number"],
    }


# @bp.route("/x")
# def x():
#     email = request.json["email"]
#     role = request.json["role"]
#     with Firebase() as fb:
#         id = fb.sign_up(email, "123456", role)
#         print(id)
#     return id


@bp.route("/refresh", methods=["GET"])  ## TODO to remove
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    resp = jsonify({"status": "SUCCESS"})
    set_access_cookies(resp, access_token)
    return resp, 200
