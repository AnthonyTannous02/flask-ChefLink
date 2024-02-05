from flask import Flask

app = Flask(__name__)

def run_app():
    from auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    
    return app.run(debug=True, host="0.0.0.0", port="5000")

if __name__ == "__main__":
    run_app()