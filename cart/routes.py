from cart import bp
from flask_jwt_extended import current_user, jwt_required
from sb_interface import SpringBoot as sb

@bp.route("/get_active_cart", methods=["GET"])
@jwt_required()
def get_active_cart():
    try:
        order = sb.get_active_cart(current_user["uUID"])
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400
    return {"status": "SUCCESS", "data": order}, 200