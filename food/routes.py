from food import bp
from food.sb_interface import SpringBoot as sb
from flask_jwt_extended import jwt_required


@bp.route("/get_food_by_perk", methods=["GET"])
@jwt_required(optional=True)
def food_by_perk():
    try:
        perks, foods = sb.get_explore_foods_by_perk(10)
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400
    return {"status": "SUCCESS", "data": {"perks": list(perks), "foods": foods}}, 200


@bp.route("/get_food_by_cuisine", methods=["GET"])
@jwt_required(optional=True)
def food_by_cuisine():
    try:
        cuisines, foods = sb.get_explore_foods_by_cuisine(10)
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400
    return {"status": "SUCCESS", "data": {"perks": list(cuisines), "foods": foods}}, 200
