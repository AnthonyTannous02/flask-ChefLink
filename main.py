from flask import Flask
from flask_login import LoginManager
from flask_session import Session

app = Flask(__name__)
app.config["SPRING_BOOT_URL"] = "http://10.31.197.153:8080"

session = Session(app)
login_manager = LoginManager()

from auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth")

# @login_manager.user_loader
# def load_user(user_id):
#     try:
#         return 
#     except:
#         return

app.run(debug=True, host="0.0.0.0", port="5000")