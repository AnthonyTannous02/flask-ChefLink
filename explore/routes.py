from explore import bp

@bp.route("/")
def test():
    return {"hi": "hi"}