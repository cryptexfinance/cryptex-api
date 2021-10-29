from flask import Flask

from routes.tokens import tokens_api


def create_app():
    app = Flask(__name__)

    app.register_blueprint(tokens_api)

    return app


new_app = create_app()
