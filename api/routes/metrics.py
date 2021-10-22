import os

from flask import Blueprint
from flask import abort

from controllers.metrics_controller import MetricsController
from routes import INFURA_KEY
from static.contracts import CONTRACTS

metrics_api = Blueprint("api", __name__, url_prefix="/metrics")


@metrics_api.route("/tokens/<token>/metrics", methods=["GET"])
def get_metrics(token: str) -> dict:
    """
    :param token: Token to get metrics for, either CTX or TCAP
    :return: Metrics for the token as a dict
    """
    pass


@metrics_api.route("/tokens/<token>/metrics/apy", methods=["GET"])
def get_apy(token: str) -> dict:
    """
    :param token: Token to get stakign APY for, either CTX or TCAP
    :return: APY percentage for the token as an int (eg. 28 for 28%)
    """
    controller = MetricsController.infura(
        project_id=os.environ.get(INFURA_KEY),
    )

    try:
        contract = CONTRACTS[token]()
    except KeyError:
        abort(404)
        raise Exception(f"Unable to get total supply for token '{token}'.")

    return controller.get_apy(contract=contract)
