from flask import Flask

from .frontend import frontend

def create_app():
    app = Flask(__name__)
    app.register_blueprint(frontend)
    return app
