from flask import Flask

from routes.cmc import cmc_api


def create_app():
    app = Flask(__name__)

    app.register_blueprint(cmc_api)

    return app


new_app = create_app()
