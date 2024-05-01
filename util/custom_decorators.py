from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def chef_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if "role" in claims and claims["role"] == "chef":
                return fn(*args, **kwargs)
            else:
                return {"error": "CHEF_REQUIRED", "status": "FAIL"}, 403
        return decorator
    return wrapper