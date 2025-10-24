from db import db
from config import Config
from routes import register_routes
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    register_routes(app)
    @app.route("/")
    def home():
        return "server started"
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)