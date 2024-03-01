from food import bp
from food.sb_interface import SpringBoot as sb

@bp.route("/")
def test():
    resp = sb.get_explore_foods_by_cuisine(10)
    return {"test": resp}