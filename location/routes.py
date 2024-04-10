from flask import request
from location import bp
from location.sb_interface import SpringBoot
from location.mg_interface import Mongo
from flask_jwt_extended import jwt_required, current_user

@bp.route("/get_locations", methods=["GET"])
@jwt_required()
def get_locations():
    try:
        with SpringBoot() as sb:
            loc_ids = sb.get_loc_ids(current_user["uUID"])
            print(loc_ids)
            with Mongo() as mg:
                locations = mg.get_locations(loc_ids)
                return {"status": "SUCCESS", "data": locations}, 200
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400


@bp.route("/get_location_by_id", methods=["GET"])
@jwt_required()
def get_location_by_id():
    try:
        loc_id = request.json["id_location"]
        with Mongo() as mg:
            location_data = mg.get_location_by_id(loc_id)
            return {"status": "SUCCESS", "data": location_data}, 200
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400


@bp.route("/add_location", methods=["POST"])
@jwt_required()
def add_location():
    try:
        location = request.json
        with Mongo() as mg:
            mg.add_location(current_user["uUID"], location)
        return {"status": "SUCCESS"}, 200
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400


@bp.route("/remove_location", methods=["DELETE"])
@jwt_required()
def remove_location():
    try:
        location_id = request.json["id_location"]
        with Mongo() as mg:
            mg.remove_location(current_user["uUID"], location_id)
        return {"status": "SUCCESS"}, 200
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400