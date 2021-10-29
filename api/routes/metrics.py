import os

from flask import Blueprint
from flask import abort
from flask import jsonify
from flask import Response

from controllers.metrics_controller import MetricsController
from routes import INFURA_KEY
from static.contracts import CONTRACTS

metrics_api = Blueprint("metrics_api", __name__, url_prefix="/metrics")


@metrics_api.route("/tokens/<token>", methods=["GET"])
def get_all_metrics(token: str) -> Response:
    """
    :param token: Token to get metrics for, either CTX or TCAP
    :return: JSON response containing all metrics for a given token
    """
    controller = MetricsController.infura(
        project_id=os.environ.get(INFURA_KEY),
    )

    try:
        contract = CONTRACTS[token]()
    except KeyError:
        abort(404)
        raise Exception(f"Unable to get total supply for token '{token}'.")

    apy = controller.get_apy(contract=contract)
    return jsonify({"apy_percentage": apy})


@metrics_api.route("/tokens/<token>/apy", methods=["GET"])
def get_apy(token: str) -> Response:
    """
    :param token: Token to get staking APY for, either CTX or TCAP
    :return: JSON response containing the raw APY percentage
    """
    controller = MetricsController.infura(
        project_id=os.environ.get(INFURA_KEY),
    )

    try:
        contract = CONTRACTS[token]()
    except KeyError:
        abort(404)
        raise Exception(f"Unable to get total supply for token '{token}'.")

    apy = controller.get_apy(contract=contract)
    return jsonify({"apy_percentage": apy})
