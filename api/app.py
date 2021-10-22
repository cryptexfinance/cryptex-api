from flask import Flask

from routes.cmc import cmc_api
from routes.metrics import metrics_api


def create_app():
    app = Flask(__name__)

    app.register_blueprint(cmc_api)
    app.register_blueprint(metrics_api)

    return app


new_app = create_app()
