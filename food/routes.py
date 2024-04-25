from flask import request
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


@bp.route("/get_food_by_type", methods=["GET"])
@jwt_required(optional=True)
def food_by_type():
    try:
        with SpringBoot() as sb:
            types, foods = sb.get_explore_foods_by_type(10)
            return {
                "status": "SUCCESS",
                "data": {"types": list(types), "foods": foods},
            }, 200
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400


@bp.route("/get_ingred_options", methods=["GET"])
def get_ingred_options():
    try:
        food_id = request.args['food_id']
        with SpringBoot() as sb:
            ingreds = sb.get_ingred_options(food_id)
            return {"status": "SUCCESS", "data": ingreds}, 200
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400


@bp.route("/search_food", methods=["GET"])
def search_food():
    try:
        search: str = request.args["search"]
        with Mongo() as mg:
            foods = mg.search_food(search)
            return {"status": "SUCCESS", "data": foods}, 200
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400


@bp.route("/search_chefs", methods=["GET"])
def search_chefs():
    try:
        search: str = request.args["search"]
        with Mongo() as mg:
            chefs = mg.search_chefs(search)
            return {"status": "SUCCESS", "data": chefs}, 200
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400


@bp.route("/filter_food_by", methods=["GET"])
def filter_food_by():
    try:
        filter = request.args["filter"]
        select = request.args["select"]
    except:
        return {
            "status": "FAIL",
            "error": "MISSING_PARAMS",
            "msg": "filter and select are required",
        }, 400
    
    try:
        if filter not in ["cuisine", "type", "perks"]:
            return {
                "status": "FAIL",
                "error": "INVALID_FILTER",
                "msg": "Should be either: 'cuisine', 'type', 'perks'",
            }, 400
        with Mongo() as mg:
            foods = mg.filter_food_by(filter, select)
            return {"status": "SUCCESS", "data": foods}, 200
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400


@bp.route("/get_food_min_info", methods=["GET"])
def get_food_min_info():
    try:
        food_ids = request.json["food_ids"]
        with Mongo() as mg:
            food = mg.get_food_min_info(food_ids)
            return {"status": "SUCCESS", "data": food}, 200
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400


@bp.route("/get_food_full_info", methods=["GET"])
def get_food_full_info():
    try:
        food_ids = request.json["food_ids"]
        with Mongo() as mg:
            food = mg.get_food_full_info(food_ids)
            return {"status": "SUCCESS", "data": food}, 200
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400


@bp.route("/get_food_and_reviews", methods=["GET"])
def get_food_and_reviews():
    try:
        food_id = request.args["food_id"]
        with SpringBoot() as sb:
            food = sb.get_food_and_reviews(food_id)
            return {"status": "SUCCESS", "data": food}, 200
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400


# @bp.route("/search_food_by_chef", methods=["GET"])
# def search_food_by_chef():
#     try:
#         chef: str = request.json["chef"]
#     except:
#         return {
#             "status": "FAIL",
#             "error": "MISSING_PARAMS",
#             "msg": "chef is required",
#         }, 400
    
#     try:
#         with Mongo() as mg:
#             foods: list = mg.search_food_by_chef(chef)
#             return {"status": "SUCCESS", "data": foods}, 200
#     except Exception as e:
#         return {"status": "FAIL", "error": str(e)}, 400