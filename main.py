from flask import Flask

app = Flask(__name__)
app.config["SPRING_BOOT_URL"] = "http://10.31.197.153:8080"


from auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth")

# return app.run(debug=True, host="0.0.0.0", port="5000")