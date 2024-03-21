from flask_pymongo import PyMongo
from flask import current_app, g, request
from food import bp
from food.sb_interface import SpringBoot
from food.mg_interface import Mongo
from flask_jwt_extended import jwt_required


@bp.route("/get_food_by_perk", methods=["GET"])
@jwt_required(optional=True)
def food_by_perk():
    try:
        perks = set()
        foods = []
        with SpringBoot() as sb:    
            perks, foods = sb.get_explore_foods_by_perk(10)
            return {
                "status": "SUCCESS",
                "data": {"perks": list(perks), "foods": foods},
            }, 200
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400


@bp.route("/get_food_by_cuisine", methods=["GET"])
@jwt_required(optional=True)
def food_by_cuisine():
    try:
        with SpringBoot() as sb:
            cuisines, foods = sb.get_explore_foods_by_cuisine(10)
            return {
                "status": "SUCCESS",
                "data": {"cuisines": list(cuisines), "foods": foods},
            }, 200
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400


@bp.route("get_ingred_options", methods=["GET"])
def get_ingred_options():
    try:
        food_id = request.json["food_id"]
        with SpringBoot() as sb:
            ingreds = sb.get_ingred_options(food_id)
            return {"status": "SUCCESS", "data": ingreds}, 200
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400


# @bp.route("/test")
# def test():
#     # try:
        
#     # except Exception as e:
#     #     return {"status": "FAIL", "error": str(e)}, 400
#     with Mongo() as mg:
#         resp = mg.get_bookmarks("4QjdrkzJfTMcTKgiQrdx3dAaCbC2")
#         print(resp)

    
    return {"status": "SUCCESS", "msg": "resp"}, 200