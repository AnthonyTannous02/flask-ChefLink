from flask import Flask, jsonify
from load_dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import (
        JWTManager, get_jwt, set_access_cookies, unset_jwt_cookies,
        get_jwt_identity, create_access_token,
    )
from datetime import datetime, timezone, timedelta
import os

load_dotenv()

app = Flask(__name__)
app.config["SPRING_BOOT_URL"] = os.getenv("SPRING_BOOT_URL")
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_COOKIE_SECURE"] = True
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

CORS(app, supports_credentials=True)
jwt = JWTManager(app)
jwt.init_app(app)

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return {"uUID": identity}

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response

@jwt.expired_token_loader
def expired_token_callback(x, y):
    resp = jsonify({"status": "FAIL", "error": "TOKEN_EXPIRED"})
    unset_jwt_cookies(resp)
    return resp, 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {"status": "FAIL", "error": "INVALID_TOKEN"}, 401

@jwt.unauthorized_loader
def unauthorized_token_callback(error):
    return {"status": "FAIL", "error": "UNAUTHORIZED"}, 401

from auth import bp as auth
from explore import bp as explore

app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(explore, url_prefix="/explore")

app.run(debug=True, host="0.0.0.0", port="5000", threaded=True, load_dotenv=True)
