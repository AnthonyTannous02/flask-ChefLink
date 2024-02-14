from explore import bp

@bp.route("/")
def test():
    return {"test": "test"}