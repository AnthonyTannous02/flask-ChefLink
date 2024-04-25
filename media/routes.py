from media import bp
from flask import request
from media.bucket_interface import BucketInterface

## TODO Improve by providing one for Users


@bp.route("/upload_image", methods=["POST"])
def upload_image():
    try:
        path = request.form["path"]
        image = request.files["image"]
        with BucketInterface() as bi:
            if bi.upload_image(image, path):
                bi.gen_url(path)
            else:
                raise Exception("UPLOAD_FAILED")
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400
    return {"status": "SUCCESS"}, 200


@bp.route("/remove_image", methods=["DELETE"])
def remove_image():
    try:
        path = request.json["path"]
        with BucketInterface() as bi:
            if not bi.remove_image(path):
                raise Exception("NOT_FOUND")
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400
    return {"status": "SUCCESS"}, 200


@bp.route("/generate_image_url", methods=["GET"])
def generate_image_url():
    try:
        path = request.args["path"]
        with BucketInterface() as bi:
            url = bi.gen_url(path)
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}, 400
    return {"status": "SUCCESS", "data": url}, 200
