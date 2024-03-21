from cart import bp
from flask_jwt_extended import current_user, jwt_required
from sb_interface import SpringBoot

@bp.route("/get_active_cart", methods=["GET"]) ## TODO Later to show the cart in the cart page
@jwt_required()
def get_active_cart():
    try:
        cart = None
        with SpringBoot() as sb:
            cart = sb.get_active_cart(current_user["uUID"])
            if cart is None:
                cart = sb.create_cart(current_user["uUID"])
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400
    return {"status": "SUCCESS", "data": cart}, 200