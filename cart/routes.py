from flask import request, current_app
from cart import bp
from flask_jwt_extended import current_user, jwt_required
from cart.sb_interface import SpringBoot
from cart.mg_interface import Mongo
from util.deliv_sim import DelivSim


@bp.route("/get_stand_by_cart_id", methods=["GET"])  ## TODO Later to show the cart in the cart page
@jwt_required()
def get_stand_by_cart():
    try:
        cart = None
        with Mongo() as mg:
            cart = mg.get_stand_by_cart(current_user["uUID"])
            if cart is None:
                cart = mg.create_cart(current_user["uUID"])
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400
    return {"status": "SUCCESS", "data": cart}, 200


@bp.route("/add_to_cart", methods=["POST"])
@jwt_required()
def add_to_cart():
    try:
        req = request.json
        food_id = req["food_id"]
        options = req["options"]
        spec_inst = req["special_instructions"]
        qty = req["quantity"]
        with Mongo() as mg:
            mg.add_to_cart(current_user["uUID"], food_id, options, spec_inst, qty)
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400
    return {"status": "SUCCESS"}, 200


@bp.route("/remove_from_cart", methods=["DELETE"])
@jwt_required()
def remove_from_cart():
    try:
        req = request.json
        bundle_id = req["bundle_id"]
        with Mongo() as mg:
            cart = mg.get_stand_by_cart(current_user["uUID"], True)
            if cart is None:
                raise Exception("NO_CURRENT_CART")
            mg.remove_from_cart(cart["iD"], bundle_id)
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400
    return {"status": "SUCCESS"}, 200


@bp.route("/get_cart_details", methods=["GET"])
@jwt_required()
def get_cart_details():
    try:
        with Mongo() as mg:
            cart = mg.get_stand_by_cart(current_user["uUID"])

            if cart is None:
                cart = mg.create_cart(current_user["uUID"])
            cart_details = mg.get_cart_details(cart)
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400
    return {"status": "SUCCESS", "data": cart_details}, 200


@bp.route("/delete_cart", methods=["DELETE"])
@jwt_required()
def delete_cart():
    try:
        with Mongo() as mg:
            mg.delete_cart(current_user["uUID"])
    except Exception as e:
        print(str(e))
        return {"status": "FAIL", "error": str(e)}, 400
    return {"status": "SUCCESS"}, 200


@bp.route("/update_current_cart_attribute", methods=["PUT"])
@jwt_required()
def update_current_cart_attribute():
    try:
        query = request.json
        cart = None
        with Mongo() as mg:
            cart = mg.get_stand_by_cart(current_user["uUID"], True)
            if cart is None:
                raise Exception("NO_CURRENT_CART")
            mg.update_current_cart_attribute(cart["iD"], query, current_user["role"])
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400
    return {"status": "SUCCESS"}, 200


@bp.route("/checkout_cart", methods=["POST"])
@jwt_required()
def checkout_cart():
    try:
        with Mongo() as mg:
            cart = mg.get_stand_by_cart(current_user["uUID"], False)
            if cart is None:
                raise Exception("NO_CART_ACTIVE")
            mg.checkout_cart(cart, current_user["role"])
            # with DelivSim(
            #     time=10, 
            #     callback=mg.deliver_order, 
            #     args=cart["iD"], 
            #     app=current_app._get_current_object()
            # ) as d:
            #     d.simulate()
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400
    return {"status": "SUCCESS"}, 200


@bp.route("/place_order", methods=["POST"])
@jwt_required()
def place_order():
    try:
        with Mongo() as mg:
            cart = mg.get_stand_by_cart(current_user["uUID"], False)
            if cart is None:
                raise Exception("NO_CART_ACTIVE")
            mg.place_order(cart, current_user["uUID"], current_user["role"])
            # with DelivSim(
            #     time=10, 
            #     callback=mg.deliver_order, 
            #     args=cart["iD"], 
            #     app=current_app._get_current_object()
            # ) as d:
            #     d.simulate()
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400
    return {"status": "SUCCESS"}, 200


@bp.route("/get_order_history", methods=["GET"])
@jwt_required()
def get_order_history():
    try:
        with Mongo() as mg:
            order_history = mg.get_order_history(current_user["uUID"])
    except Exception as e:
        print(str(e))
        return {"status": "FAIL", "error": str(e)}, 400
    return {"status": "SUCCESS", "data": order_history}, 200


@bp.route("/get_bundle_info", methods=["POST"])
def get_bundle_info():
    try:
        bundle_ids: list = request.json["bundle_ids"]
        with Mongo() as mg:
            bundle_info = mg.get_bundle_info(bundle_ids)
    except Exception as e:
        print(str(e))
        return {"status": "FAIL", "error": str(e)}, 400
    return {"status": "SUCCESS", "data": bundle_info}, 200